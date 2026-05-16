import random
import json
import string

def generate_s1(n):
    questions = []
    for i in range(n):
        top = [random.choice(string.ascii_uppercase) for _ in range(4)]
        bottom = []
        for _ in range(4):
            if random.random() < 0.4:
                bottom.append(random.choice(top).lower())
            else:
                bottom.append(random.choice(string.ascii_lowercase))
        
        matches = 0
        for char in bottom:
            if char.upper() in top:
                matches += 1
        
        questions.append({
            "id": 100 + i + 1,
            "type": "matching",
            "topRow": top,
            "bottomRow": bottom,
            "options": ["0", "1", "2", "3", "4"],
            "answer": matches
        })
    return questions

def generate_s2(n):
    names = ["Lia", "Tia", "Yuli", "Budi", "Andi", "Caca", "Dedi", "Eka", "Fani", "Gita"]
    questions = []
    for i in range(n):
        n_sel = random.sample(names, 3)
        a, b, c = n_sel
        templates = [
            {
                "q": f"{a} lebih kuat daripada {b}\n{a} lebih lemah daripada {c}\nSiapa yang terkuat?",
                "opts": [a, b, c],
                "ans": 2
            },
            {
                "q": f"{a} lebih tinggi daripada {b}\n{b} lebih tinggi daripada {c}\nSiapa yang paling pendek?",
                "opts": [a, b, c],
                "ans": 2
            },
            {
                "q": f"{a} lebih cepat daripada {b}\n{c} lebih lambat daripada {b}\nSiapa yang tercepat?",
                "opts": [a, b, c],
                "ans": 0
            },
            {
                "q": f"{a} lebih murah daripada {b}\n{a} lebih mahal daripada {c}\nSiapa yang paling murah?",
                "opts": [a, b, c],
                "ans": 2
            }
        ]
        t = random.choice(templates)
        questions.append({
            "id": 200 + i + 1,
            "type": "text",
            "question": t["q"],
            "options": t["opts"],
            "answer": t["ans"]
        })
    return questions

def generate_s3(n):
    questions = []
    for i in range(n):
        while True:
            # Pick a starting character
            start_idx = random.randint(0, 25 - 8) # leave room for distances
            char1 = string.ascii_uppercase[start_idx]
            
            # Distance 1-4
            dist1 = random.randint(1, 4)
            char2 = string.ascii_uppercase[start_idx + dist1]
            
            # Distance 1-4, but different from dist1
            dist2 = random.randint(1, 4)
            while dist2 == dist1:
                dist2 = random.randint(1, 4)
            
            char3 = string.ascii_uppercase[start_idx + dist1 + dist2]
            seq = [char1, char2, char3]
            
            d1 = dist1
            d2 = dist2
            if d1 != d2:
                break
        
        # Closest adjacent pair
        if d1 < d2:
            ans_idx = 0 # first item is outermost in pair 0-1
        else:
            ans_idx = 2 # last item is outermost in pair 1-2
            
        questions.append({
            "id": 300 + i + 1,
            "type": "sequence",
            "sequence": seq,
            "question": "Pilih satu huruf terluar yang merupakan bagian dari pasangan dengan jarak alfabet terdekat:",
            "options": seq,
            "answer": ans_idx
        })
    return questions

def generate_s4(n):
    questions = []
    for i in range(n):
        while True:
            # max value 30, max dist 4
            s1 = random.randint(0, 30)
            
            dist1 = random.randint(1, 4)
            # randomly go up or down, but keep within [0, 30]
            if s1 + dist1 <= 30 and (s1 - dist1 < 0 or random.random() < 0.5):
                s2 = s1 + dist1
            else:
                s2 = s1 - dist1
                
            dist2 = random.randint(1, 4)
            while dist2 == dist1:
                dist2 = random.randint(1, 4)
                
            if s2 + dist2 <= 30 and (s2 - dist2 < 0 or random.random() < 0.5):
                s3 = s2 + dist2
            else:
                s3 = s2 - dist2
            
            seq = [s1, s2, s3]
            d1 = abs(s1 - s2)
            d2 = abs(s2 - s3)
            if d1 != d2 and all(0 <= x <= 30 for x in seq):
                break
        
        # Largest adjacent pair
        if d1 > d2:
            ans_idx = 0 # first item is outermost in pair 0-1
        else:
            ans_idx = 2 # last item is outermost in pair 1-2
            
        questions.append({
            "id": 400 + i + 1,
            "type": "sequence",
            "sequence": seq,
            "question": "Pilih satu angka terluar yang merupakan bagian dari pasangan (berdekatan) dengan selisih terbesar:",
            "options": [str(x) for x in seq],
            "answer": ans_idx
        })
    return questions

def generate_s5(n):
    syms = ['F', 'ꟻ', 'Ⅎ', 'R', 'Я', 'ꓤ']
    questions = []
    for i in range(n):
        top = [random.choice(syms) for _ in range(3)]
        bottom = []
        for _ in range(3):
            if random.random() < 0.5:
                bottom.append(top[len(bottom)])
            else:
                bottom.append(random.choice(syms))
        
        matches = 0
        for j in range(3):
            if top[j] == bottom[j]:
                matches += 1
                
        questions.append({
            "id": 500 + i + 1,
            "type": "matching",
            "topRow": top,
            "bottomRow": bottom,
            "options": ["0", "1", "2", "3"],
            "answer": matches
        })
    return questions

def generate_s6(n):
    questions = []
    for i in range(n):
        ops = ['+', '-', '*', '/']
        op = random.choice(ops)
        if op == '+':
            a, b = random.randint(10, 100), random.randint(10, 100)
            q = f"{a} + {b} = ..."
            ans_val = a + b
        elif op == '-':
            a, b = random.randint(50, 150), random.randint(10, 50)
            q = f"{a} - {b} = ..."
            ans_val = a - b
        elif op == '*':
            a, b = random.randint(2, 12), random.randint(2, 12)
            q = f"{a} x {b} = ..."
            ans_val = a * b
        else:
            b = random.randint(2, 12)
            ans_val = random.randint(2, 12)
            a = b * ans_val
            q = f"{a} / {b} = ..."
        
        # Add some variety with fractions
        if random.random() < 0.3:
            denom = random.randint(2, 9)
            num = random.randint(1, denom*5)
            whole = random.randint(10, 30)
            q = f"{whole} - {num}/{denom} = ..."
            # ans = whole - num/denom
            # options will be strings like "26 2/7"
            # let's just make one question like this or stick to simple
            pass

        opts = [ans_val, ans_val + random.randint(1, 5), ans_val - random.randint(1, 5), ans_val + 10]
        random.shuffle(opts)
        ans_idx = opts.index(ans_val)
        
        questions.append({
            "id": 600 + i + 1,
            "type": "text",
            "question": q,
            "options": [str(x) for x in opts],
            "answer": ans_idx
        })
    return questions

data = {
    "1": generate_s1(60),
    "2": generate_s2(50),
    "3": generate_s3(72),
    "4": generate_s4(60),
    "5": generate_s5(60),
    "6": generate_s6(40)
}

print("export const QUESTIONS = " + json.dumps(data, indent=2, ensure_ascii=False))
