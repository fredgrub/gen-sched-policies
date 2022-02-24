from __future__ import print_function
import numpy as np
import scipy.optimize as sp
import sys

def extract_data(filename):
    score = []
    p = []
    q = []
    r = []

    with open(filename, 'r') as input_file:
        input_lines = input_file.readlines()

        for i, line in enumerate(input_lines):
            row = line.split(",")
            p.append(float(row[0]))
            q.append(float(row[1]))
            r.append(float(row[2]))
            score.append(float(row[3]))
        
    np_p = np.array(p)
    np_q = np.array(q)
    np_r = np.array(r)
    np_score = np.array(score).astype(dtype=np.float32)
    
    n_score = len(input_lines)
    
    return np_p, np_q, np_r, np_score, n_score

def linear(
    x,
    d0, a1, b1, c1
    ):
    p, q, r = x
    return d0 + a1 * p + b1 * q + c1 * r

def quadratic(
    x,
    d0, a1, b1, c1,
    a2, b2, c2, alp11
    ):
    p, q, r = x
    return linear(x, d0, a1, b1, c1) + \
        a2 * p**2 + b2 * q**2 + c2 * r**2 + alp11 * p*q

def cubic(
    x,
    d0, a1, b1, c1,
    a2, b2, c2, alp11,
    a3, b3, c3, alp21, alp12
    ):
    p, q, r = x
    return quadratic(x, d0, a1, b1, c1, a2, b2, c2, alp11) + \
        a3 * p**3 + b3 * q**3 + c3 * r**3 + alp21 * (p**2)*q + alp12 * p*(q**2)

def quartic(
    x,
    d0, a1, b1, c1,
    a2, b2, c2, alp11,
    a3, b3, c3, alp21, alp12,
    a4, b4, c4, alp31, alp13, alp22
):
    p, q, r = x
    return cubic(x, d0, a1, b1, c1, a2, b2, c2, alp11, a3, b3, c3, alp21, alp12) + \
        a4 * p**4 + b4 * q**4 + c4 * r**4 + \
        alp31 * (p**3)*q + alp13 * p*(q**3) + alp22 * (p*q)**2

def run_regression(func, p, q, r, score, num_data):
    # sigma
    w = np.zeros(num_data)
    for i in range(num_data):
        w[i] = 1.0 / (p[i] * q[i])

    # regression
    popt, pcov = sp.curve_fit(
        func, (p, q, r), score, sigma=w, absolute_sigma=True
        )
    
    # error
    residuals = 0.0
    for i in range(num_data):
        residuals += np.absolute(
            score[i] - func((p[i], q[i], r[i]), *popt)
            )
    score = (residuals/num_data)
    #print("%.2E" % score)
    
    return popt, score

def main():
    p, q, r, score, num_data = extract_data(sys.argv[1])
    #print(p[0], q[0], r[0], score[0], num_data)

    polynomials = [linear, quadratic, cubic, quartic]
    poly_labels = ["Linear", "Quadratic", "Cubic", "Quartic"]

    for i, polynomial in enumerate(polynomials):
        parameters, error = run_regression(polynomial, p, q, r, score, num_data)
        print(poly_labels[i])
        print(parameters)
        print('ERROR = %.2E\n' % error)

if __name__ == "__main__":
    main()