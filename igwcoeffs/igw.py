# -*- coding: utf-8 -*-
import os
from email.mime.text import MIMEText

import numpy as np
from django.core.mail import EmailMessage
from django.core.mail import send_mail
from django.template.loader import get_template
from scipy import integrate
from scipy.interpolate import interp1d
from scipy.integrate import odeint
from scipy import constants
from tempfile import TemporaryFile
from django.core.files import File

# acceleration of gravity
from igwcoeffs.models import Calculation
from celery import shared_task

GG = constants.g
PI = constants.pi

NOT_FOUND_CALCULATION = -1
NOT_ENOUGH_PARAMS = -2

epsilon_f = 1e-4
epsilon_t = 1e-4

epsilon_t_rough = 1e-4
epsilot_t_exact = 1e-5


def get_rho(temp, sal):
    """
    Get density, Foffonoff state sea water
    :param temp:
    :param sal:
    :return: rho
    """
    R00 = 1000
    A = 999.842594 + 6.793952e-2*temp - 9.09529e-3*temp**2 + 1.001685e-4*temp**3 - 1.120083e-6*temp**4 + 6.536332e-9*temp**5
    B = 8.24493e-1 - 4.0899e-3*temp + 7.6438e-5*temp**2 - 8.2467e-7*temp**3 + 5.3875e-9*temp**4
    C = -5.72466e-3  +  1.0227e-4*temp - 1.6546e-6*temp**2
    D = 4.8314e-4
    E = 19652.21 + 148.4206*temp - 2.327105*temp**2 + 1.360477e-2*temp**3 - 5.155288e-5*temp**4
    F = 54.6746-.603459*temp  + 1.09987e-2*temp**2  -  6.167e-5*temp**3
    G = 7.944e-2+1.6483e-2*temp - 5.3009e-4*temp**2
    H = 3.239908  +  1.43713e-3*temp  +  1.16092e-4*temp**2 - 5.77905e-7*temp**3
    I = 2.2838e-3 - 1.0981e-5*temp - 1.6078e-6*temp**2
    J = 1.91075e-4
    M = 8.50935e-5 - 6.12293e-6*temp + 5.2787e-8*temp**2
    N = -9.9348e-7 + 2.0816e-8*temp +  9.1697e-10*temp**2
    R0 = A + B*sal + C*sal**1.5 + D*sal**2
    P = 0
    RK = E+F*sal+G*sal**1.5+(H+I*sal+J*sal**1.5)*P+(M+N*sal)*P**2
    rho = R0/(1-P/RK)-R00
    return rho


def get_bvf(rho, depth):
    """
    Get Brenta-Vaisala frequency
    :param rho:
    :param depth:
    :return: frequency
    """
    length = rho.shape[0]

    # init bvf array
    bvf = np.empty(length)
    bvf.fill(0)

    # incompressible fluid case
    r1 = rho[0]
    for i in range(length-1):
        r2 = rho[i+1]
        bvf[i] = np.sqrt(
            np.abs(
                GG*(r2 - r1)/(depth[i+1] - depth[i])/(1000 + r2)
            )
        )
        r1 = r2

    bvf[i+1] = bvf[i]

    return bvf


def handle_file(file, separator, max_row=None):
    # save file
    with open(file.name, 'wb+') as destination:
        for chunk in file.chunks():
            destination.write(chunk)

    with open(file.name) as file:
        data = file.read()

    data = data.split('\n')
    if not max_row:
        max_row = len(data)

    result = []
    for i in range(0, max_row):
        parse_row = data[i].split(separator)
        row = []
        for element in parse_row:
            if len(element) > 1:
                row.append(element)
        result.append(row)

    # remove tmp file
    os.unlink(file.name)

    if result:
        return True, result[:max_row], len(data)
    else:
        return False, 'EMPTY_FILE', 'Пустой файл'


def read_file(filename, skip_rows=0, delimiter=None):
    print("read file ", filename)
    if delimiter:
        data = np.loadtxt(filename, skiprows=skip_rows)
    else:
        data = np.loadtxt(filename, skiprows=skip_rows, delimiter=delimiter)
    return data


def sys_phi(y, z, N, c):
    phi, dphi = y
    dy = [dphi, -((N(z) / c) ** 2) * phi]
    return dy


def func_r(z, c, alpha, dif_phi, dif2_phi):
    rhs = (-alpha/c + 3 * dif_phi(z)) * dif2_phi(z)
    return rhs


def sys_f_or_tn(y, z, N, c, alpha, dif_phi, dif2_phi):
    f, df = y
    dy = [df, -((N(z) / c) ** 2) * f + func_r(z, c, alpha, dif_phi, dif2_phi)]
    return dy


def calc_coeffs_point(z_down, n_freq, num_mode=0, max_mode=1):
    max_depth = np.amax(z_down)
    max_bvf = np.amax(n_freq)
    len_data = np.size(z_down)

    # init new array
    rev_z = np.zeros(len_data)
    rev_bvf = np.zeros(len_data)

    # reverse coordinate z
    for i in range(0, len_data):
        rev_z[len_data-1-i] = max_depth - z_down[i]
        rev_bvf[len_data-1-i] = n_freq[i]

    N = interp1d(rev_z, rev_bvf, kind='cubic', fill_value="extrapolate")

    c = np.zeros(2)
    beta = np.zeros(2)
    alpha = np.zeros(2)
    alpha1 = np.zeros(2)
    for i in range(num_mode, max_mode):
        current_mode = i + 1
        print('Current mode {}'.format(current_mode))
        c[i] = max_bvf * max_depth / PI / current_mode
        dc = c[i]

        z_zer = np.zeros(max_mode + 1)
        z = np.linspace(rev_z[0], rev_z[-1], 100000)  # the points of evaluation of solution
        init_cond = [0, 0.01]  # initial value

        while True:
            zero_counter = 0
            sol = odeint(sys_phi, init_cond, z, args=(N, c[i]), rtol=[1e-4, 1e-4], atol=[1e-6, 1e-6])
            phi = sol[:, 0]
            dphi = sol[:, 1]

            n_z_grid = len(z) - 1
            for j in range(1, n_z_grid):
                if phi[j - 1] * phi[j] < 0:
                    zero_counter += 1
                    z_zer[zero_counter] = z[j - 1]
            z_zer_phi = z_zer[i]

            if np.abs(phi[-1] / np.max(phi)) <= epsilon_f:
                print('c finished')
                break
            elif dc < 1e-10:
                raise RuntimeError("Could not integrate")
            elif zero_counter <= i:
                dc /= 2
                c[i] -= dc
            elif zero_counter > i:
                dc /= 2
                c[i] += dc

        min_phi, ind_min_phi = np.min(phi), np.argmin(phi)
        # second mode, pronounced minimum
        if np.abs(min_phi) > 10**(-1):
            phi *= (-1)
            dphi *= (-1)

        max_phi, ind_max_phi = np.max(phi), np.argmax(phi)
        min_phi, ind_min_phi = np.min(phi), np.argmin(phi)

        # normalization
        phi /= max_phi
        dphi /= max_phi

        min_phi /= max_phi
        max_phi /= max_phi

        z_max_phi = z[ind_max_phi]
        z_min_phi = z[ind_min_phi]

        # coeffs
        num_beta = phi*phi
        denom = dphi*dphi
        num_alpha = denom*dphi

        beta[i] = (c[i]/2) * np.trapz(num_beta, z)/np.trapz(denom, z)
        alpha[i] = (3*c[i]/2) * np.trapz(num_alpha, z)/np.trapz(denom, z)

        # alpha 1
        t_end_prev = 0.0
        init_cond = [0, 0.01]  # initial value

        dif_phi = interp1d(z, dphi, kind='cubic', fill_value="extrapolate")
        temp = np.diff(dphi)/np.diff(z)
        d2phi = np.append(temp, temp[-1])
        dif2_phi = interp1d(z,d2phi, kind='cubic', fill_value="extrapolate")

        while True:
            sol = odeint(sys_f_or_tn, init_cond, z, args=(N, c[i], alpha[i], dif_phi, dif2_phi),
                         rtol=[1e-4, 1e-4], atol=[1e-6, 1e-6])
            t = sol[:, 0] # F or Tn
            dt = sol[:, 1] # dF or dTn

            t_zmax = t[ind_max_phi]
            coef = -np.sign(phi[ind_max_phi])

            t_z_phi = t + coef * t_zmax * phi
            dt_z_phi = dt + coef * t_zmax * dphi

            t_end = t_z_phi[n_z_grid]

            dt_1 = dt_z_phi[0]

            # temp solution for small depths
            if np.max(z_down) <= 20:
                epsilon_t = epsilon_t_rough
            else:
                epsilon_t = epsilot_t_exact

            if np.abs(t_end - t_end_prev) <= epsilon_t or (np.abs(t_end / np.max(np.abs(t_z_phi))) <= epsilon_t):
                print('Tn or F finished')
                break

            init_cond = [0, dt_1]
            t_end_prev = t_end

        # Chapter 4 Pelinovsky et al 2007
        term1_a1 = 9 * c[i] * dt_z_phi * denom
        term2_a1 = -6 * c[i] * denom * denom
        term3_a1 = 5 * alpha[i] * num_alpha
        term4_a1 = -4 * alpha[i] * dt_z_phi * dphi
        term5_a1 = -(alpha[i])**2 / c[i] * denom
        num_alpha1 = term1_a1 + term2_a1 + term3_a1 + term4_a1 + term5_a1
        alpha1[i] = 1/2 * np.trapz(num_alpha1, z) / np.trapz(denom, z)

        # revert z:
        z_grid_tmp = z
        phi_tmp = phi
        dphi_tmp = dphi
        t_z_phi_tmp = t_z_phi

        # reverse coordinate z
        len_z = len(z)
        for m in range(0, len_z):
            z[len_data - 1 - i] = max_depth - z_grid_tmp[m]
            phi[len_data - 1 - i] = phi_tmp[m]
            dphi[len_data - 1 - i] = -dphi_tmp[m]      # sign changed
            t_z_phi[len_data - 1 - i] = t_z_phi_tmp[m]

        t_z_phi_norm = t_z_phi / np.max(np.abs(t_z_phi))
        z_max_phi = max_depth - z_max_phi
        z_min_Phi = max_depth - z_min_phi
        z_zer_phi = max_depth - z_zer_phi

        result = [c[i], beta[i], alpha[i], alpha1[i], z_max_phi, z_min_Phi, z_zer_phi]
        return result


def sys_phi_new(z, y, c, N):
    phi, dphi = y
    dy = [dphi, -((N(z) / c) ** 2) * phi]
    return dy


@shared_task()
def run_calculation(id):
    try:
        calc = Calculation.objects.get(id=id)
    except Calculation.DoesNotExist:
        return NOT_FOUND_CALCULATION

    if calc.parse_separator == Calculation.SPACE:
        data = read_file(calc.source_file,
                         calc.parse_start_from,
                         calc.parse_separator)
    else:
        data = read_file(calc.source_file,
                         calc.parse_start_from)

    # parse data
    fields = calc.parse_file_fields.split(',')
    lon = np.array([])
    lat = np.array([])
    depth = np.array([])
    z_down = np.array([])
    temp = np.array([])
    sal = np.array([])
    rho = np.array([])
    n_freq = np.array([])
    for i, field in enumerate(fields):
        if field == 'lon':
            lon = data[:, i]
        elif field == 'lat':
            lat = data[:, i]
        elif field == 'max_depth':
            depth = data[:, i]
        elif field == 'depth':
            z_down = data[:, i]
        elif field == 'temperature':
            temp = data[:, i]
        elif field == 'salinity':
            sal = data[:, i]
        elif field == 'density':
            rho = data[:, i]
        elif field == 'bvf':
            n_freq = data[:, i]

    if not n_freq.size:
        if rho.size and z_down.size:
            n_freq = get_bvf(rho, z_down)
        elif temp.size and sal.size and z_down.size:
            rho = get_rho(temp, sal)
            n_freq = get_bvf(rho, z_down)
        else:
            return NOT_ENOUGH_PARAMS

    if calc.types == Calculation.TYPE_POINT:
        num_mode = 0
        max_mode = 1
        if calc.mode == Calculation.SECOND_MODE:
            num_mode = 1
            max_mode = 2

        result = calc_coeffs_point(z_down, n_freq, num_mode=num_mode, max_mode=max_mode)

        title = ''
        output = []
        if lon.size and lat.size:
            title += '    lon    lat'
            output.extend([lon[0], lat[0]])
        if depth.size:
            title += '    max_depth    '
            output.append(depth[0])
        if result:
            title += '    c    beta    alpha    alpha1    z_max_phi    z_min_Phi    z_zer_phi\n'
            output.extend(result)

        fname = 'result_{}.txt'.format(calc.id)
        outfile = TemporaryFile()
        x = np.array(output)
        np.savetxt(outfile, x, newline='     ', fmt='%8.5f', comments='', header=title)

        # save result to file
        calc.result_file.save(fname, File(outfile))
        calc.save()

        # send email with attachments
        if calc.email:
            send_result_by_email(calc.id, calc.result_file, calc.email, 'Результат расчёта # {}'.format(calc.id))

        return True, calc.result_file.url
    elif calc.types == Calculation.TYPE_SECTION:
        # TBD
        pass


def send_result_by_email(id, outfile, email, title):
    template_text = get_template('igwcoeffs/send_result_email.html')
    context = {
        'id': id,
    }

    recipient_list = [email]
    body_text = template_text.render(context)

    message = EmailMessage(
        title,
        body_text,
        from_email='lmnad@nntu.ru',
        to=recipient_list,
    )
    message.content_subtype = "html"
    message.attach_file(outfile.path)
    message.send(fail_silently=True)