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
    t0, t1, t2, t3
    ):
    p, q, r = x
    return t0 + t1 * p + t2 * q + t3 * r

def quadratic(
    x,
    t0, t1, t2, t3,
    t4, t5, t6, t7
    ):
    p, q, r = x
    return linear(x, t0, t1, t2, t3) + \
        t4 * p**2 + t5 * q**2 + t6 * r**2 + t7 * p*q

def cubic(
    x,
    t0, t1, t2, t3,
    t4, t5, t6, t7,
    t8, t9, t10, t11,
    t12, t13
    ):
    p, q, r = x
    return quadratic(x,t0, t1, t2, t3, t4, t5, t6, t7) +\
        t8 * p**3 + t9 * q**3 + t10 * r**3 + t11 * (p**2)*q +\
        t12 * p*(q**2) + t13 * (p*q)**2

def quartic(
    x,
    t0, t1, t2, t3,
    t4, t5, t6, t7,
    t8, t9, t10, t11,
    t12, t13, t14, t15,
    t16, t17, t18, t19
):
    p, q, r = x
    return cubic(x,t0, t1, t2, t3, t4, t5, t6, t7, t8, t9, t10, t11, t12, t13)+\
        t14 * p**4 + t15 * q**4 + t16 * r**4 + \
        t17 * (p**3)*q + t18 * p*(q**3) + t19 * (p*q)**3

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
    score_file = sys.argv[1]
    p, q, r, score, num_data = extract_data(score_file)
    #print(p[0], q[0], r[0], score[0], num_data)

    print(score_file)

    polynomials = [linear, quadratic, cubic, quartic]
    poly_labels = ["Linear", "Quadratic", "Cubic", "Quartic"]

    for i, polynomial in enumerate(polynomials):
        parameters, error = run_regression(polynomial, p, q, r, score, num_data)
        print(poly_labels[i])
        print(parameters)
        print('ERROR = %.2E\n' % error)

if __name__ == "__main__":
    main()