import random
import math
random.seed()

def gcd(e,phi_n): 
    if(phi_n == 0): 
        return e 
    else: 
        return gcd(phi_n, e % phi_n) 

def egcd(a, b):
    if a == 0:
        return (b, 0, 1)
    else:
        g, y, x = egcd(b % a, a)
        return (g, x - (b // a) * y, y)

def modinv(a, m):
    g, x, y = egcd(a, m)
    if g == 1:
        return x % m

#加速計算 y = x^H mod n
def square_and_Multiply(x, H):
    H = bin(H)
    H = H[2:]
    y = 1
    l = len(H)

    for i in range(0, l):
	    y = (math.pow(y, 2)) % n
	    if (H[i] == '1'):
		    y = (y * x) % n
    return int(y)

def CRT(dq, dp, p, q, c): 
      
    # Message part 1 
    m1 = pow(c, dp, p) 
      
    # Message part 2 
    m2 = pow(c, dq, q) 
      
    qinv = modinv(q, p) 
    h = (qinv * (m1 - m2)) % p 
    m = m2 + h * q 
    return m 

def miller_rabin_test(num, round):
    if num == 2:
        return True
    if num % 2 == 0:
        return False

    r, s = 0, num - 1
    while s % 2 == 0:
        r += 1
        s //= 2
    for _ in range(round):
        a = random.randrange(2, num - 1)
        x = pow(a, s, num)
        if x == 1 or x == num - 1:
            continue
        for _ in range(r - 1):
            x = pow(x, 2, num)
            if x == num - 1:
                break
        else:
            return False
    return True

def random_prime_generator():
    prime = ''
    while(True):
        prime = '1'
        for i in range(510):
            prime = prime + str(random.randint(0,1))
        prime = prime + '1'
        prime = int(prime,2)
        #Prime test
        if miller_rabin_test(prime,5):
            break
    return prime

plaintext = input('Enter a plaintext:')
plaintext=int(plaintext)

p = random_prime_generator()
print('Generate p in random:', p)
q = random_prime_generator()
print('Generate q in random:', q)
n = p * q
phi_n = (p-1) * (q-1)
e = 0

#產生public key e
for i in range(2, phi_n):
    if gcd(i,phi_n) == 1:
        e = i
        break

#產生private key d
d = modinv(e, phi_n)

#加密
ciphertext = square_and_Multiply(plaintext, e)
print('after encryption, ciphertext:',ciphertext)

#解密
x = ciphertext
dq = pow(d, 1, q - 1) 
dp = pow(d, 1, p - 1) 
print('after decryption, plaintext:', CRT(dq, dp, p, q, x))