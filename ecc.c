#include <stdio.h>
#include <stdlib.h>
#include <string.h>

// Elliptic Curve Parameters (Adjust as needed)
#define MODULUS 97
#define A 0
#define B 7
#define G_X 2
#define G_Y 22
#define N 97

// Struct to represent a point on the elliptic curve
typedef struct {
    unsigned long long x;
    unsigned long long y;
    int infinity; // 1 if the point is at infinity, 0 otherwise
} EC_Point;

// Function Headers
unsigned long long mod_add(unsigned long long a, unsigned long long b, unsigned long long m);
unsigned long long mod_sub(unsigned long long a, unsigned long long b, unsigned long long m);
unsigned long long mod_mul(unsigned long long a, unsigned long long b, unsigned long long m);
unsigned long long mod_inv(unsigned long long a, unsigned long long m);
EC_Point point_add(EC_Point p1, EC_Point p2, unsigned long long p);
EC_Point point_double(EC_Point point, unsigned long long p_mod);
EC_Point scalar_mult(EC_Point point, unsigned long long k, unsigned long long p_mod);
void key_generation(unsigned long long *private_key, EC_Point *public_key);
void print_point(EC_Point p);
unsigned long long simple_hash(const char* message); // Function prototype

// Main Function (For Testing Scalar Multiplication)
int main() {
    printf("Starting program\n");

    // Example point on the curve (small parameters for testing)
    EC_Point G = {G_X, G_Y, 0}; // Initialize generator point G
    printf("Generator G: (%llu, %llu)\n", G.x, G.y);

    // Example message
    const char *message = "Hello, ECDSA!";
    unsigned long long private_key;
    EC_Point public_key;

    // Generate keys
    key_generation(&private_key, &public_key);

    // Sign the message
    unsigned long long k = 3; // Replace with a randomly generated k
    unsigned long long r, s;
    unsigned long long H_m = simple_hash(message);
    
    printf("Hash of message H(m): %llu\n", H_m);

    // Compute R
    EC_Point R = scalar_mult(G, k, MODULUS);
    r = R.x % N;

    printf("Computed R: (%llu, %llu), r: %llu\n", R.x, R.y, r);

    // Compute s
    unsigned long long k_inv = mod_inv(k, N);
    s = (k_inv * (H_m + private_key * r)) % N;

    printf("Signature components: r: %llu, s: %llu\n", r, s);

    // Print the signature
    printf("Signature: (r: %llu, s: %llu)\n", r, s);

    // After signing, include this in your main function for verification
    unsigned long long w = mod_inv(s, N);
    unsigned long long u1 = (H_m * w) % N;
    unsigned long long u2 = (r * w) % N;

    printf("w: %llu, u1: %llu, u2: %llu\n", w, u1, u2);

    // Compute the elliptic curve point
    EC_Point P = point_add(scalar_mult(G, u1, MODULUS), scalar_mult(R, u2, MODULUS), MODULUS);
    printf("P: (%llu, %llu)\n", P.x, P.y);

    // Verify the signature
    if (r % N == P.x % N) {
        printf("Signature is valid!\n");
    } else {
        printf("Signature is invalid!\n");
    }

    printf("Program completed successfully\n");
    return 0;
}

// Simple hash function
unsigned long long simple_hash(const char* message) {
    unsigned long long hash = 0;
    while (*message) {
        hash = (hash * 31) + *message++;
    }
    return hash % N; // Reduce to the size of the curve order
}

// (Include the rest of your existing functions here...)

// Modular Addition
unsigned long long mod_add(unsigned long long a, unsigned long long b, unsigned long long m) {
    return (a + b) % m;
}

// Modular Subtraction
unsigned long long mod_sub(unsigned long long a, unsigned long long b, unsigned long long m) {
    return (a >= b) ? (a - b) % m : (m + a - b) % m;
}

// Modular Multiplication
unsigned long long mod_mul(unsigned long long a, unsigned long long b, unsigned long long m) {
    return (a * b) % m;
}

// Modular Inverse (Extended Euclidean Algorithm)
unsigned long long mod_inv(unsigned long long a, unsigned long long m) {
    long long m0 = m, t, q;
    long long x0 = 0, x1 = 1;

    if (m == 1) return 0;
    if (a == 0) { // No modular inverse if a is 0
        printf("Error: Modular inverse of zero is undefined\n");
        exit(1);
    }

    while (a > 1) {
        q = a / m;
        t = m;

        m = a % m, a = t;
        t = x0;

        x0 = x1 - q * x0;
        x1 = t;
    }

    if (x1 < 0)
        x1 += m0;

    return x1;
}

// Point Addition
EC_Point point_add(EC_Point p1, EC_Point p2, unsigned long long p_mod) {
    if (p1.infinity) return p2;
    if (p2.infinity) return p1;

    EC_Point result;

    if (p1.x == p2.x && p1.y != p2.y) {
        result.infinity = 1;
        return result;
    }

    unsigned long long lambda;
    if (p1.x == p2.x && p1.y == p2.y) {
        return point_double(p1, p_mod);
    } else {
        unsigned long long denominator = mod_sub(p2.x, p1.x, p_mod);
        if (denominator == 0) {
            printf("Error: Division by zero in point addition\n");
            exit(1);
        }
        lambda = mod_mul(mod_sub(p2.y, p1.y, p_mod), mod_inv(denominator, p_mod), p_mod);
    }

    result.x = mod_sub(mod_mul(lambda, lambda, p_mod), mod_add(p1.x, p2.x, p_mod), p_mod);
    result.y = mod_sub(mod_mul(lambda, mod_sub(p1.x, result.x, p_mod), p_mod), p1.y, p_mod);
    result.infinity = 0;

    return result;
}

// Point Doubling
EC_Point point_double(EC_Point p, unsigned long long p_mod) {
    if (p.infinity || p.y == 0) {
        EC_Point result = {0, 0, 1};
        return result;
    }

    EC_Point result;
    unsigned long long denominator = mod_mul(2, p.y, p_mod);
    if (denominator == 0) {
        printf("Error: Division by zero in point doubling\n");
        exit(1);
    }

    unsigned long long lambda = mod_mul(
        mod_mul(3, mod_mul(p.x, p.x, p_mod), p_mod) + A,
        mod_inv(denominator, p_mod),
        p_mod
    );

    result.x = mod_sub(mod_mul(lambda, lambda, p_mod), mod_mul(2, p.x, p_mod), p_mod);
    result.y = mod_sub(mod_mul(lambda, mod_sub(p.x, result.x, p_mod), p_mod), p.y, p_mod);
    result.infinity = 0;

    return result;
}

// Scalar Multiplication (Double-and-Add Algorithm)
EC_Point scalar_mult(EC_Point p, unsigned long long k, unsigned long long p_mod) {
    EC_Point result = {0, 0, 1}; // Initialize to point at infinity
    EC_Point current = p; // Current point to be added

    while (k > 0) {
        if (k & 1) {
            // If the current bit of k is 1, add current to result
            result = point_add(result, current, p_mod);
        }
        // Double the point
        current = point_double(current, p_mod);
        // Shift k to the right
        k >>= 1;
    }

    return result;
}

// Key Generation
void key_generation(unsigned long long *private_key, EC_Point *public_key) {
    // Generate a random private key (use a real RNG for secure implementation)
    *private_key = 12345; // Placeholder for random generation
    EC_Point G = {G_X, G_Y, 0}; // Generator point

    // Calculate public key as private_key * G
    *public_key = scalar_mult(G, *private_key, MODULUS);
}

// Print EC Point
void print_point(EC_Point p) {
    if (p.infinity) {
        printf("Point at infinity\n");
    } else {
        printf("Point: (%llu, %llu)\n", p.x, p.y);
    }
}
