import sympy
from sympy import sin

x = sympy.Symbol('x')

num_freq =[2,3,5,30]
f = sin(2*x) * sin(3*x) * sin(5*x) * sin(30*x)
df = sympy.diff(f,x)

denom_freq = [1, 6, 10, 15]
g = sin(1*x) * sin(6*x) * sin(10*x) * sin(15*x)
dg = sympy.diff(g,x)

zeros = [0]
for d in denom_freq:
    z = 0
    while(z <= 1):
        z += 1
        zeros.append(2*sympy.pi*z/d)

print(
    sorted(list(set(zeros)))
)

for z in zeros:
    zf = f.evalf(subs={x: z})
    zg = g.evalf(subs={x: z})

    zdf = df.evalf(subs={x: z})
    zdg = dg.evalf(subs={x: z})

    print(z, zdf, zdg) 
