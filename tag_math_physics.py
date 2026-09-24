import os
import json
import re

# Comprehensive topic mapping rules for Mathematics
MATH_TOPICS = {
    "Algebra, Indices, Logarithms & Complex Numbers": [
        r"\bi\b", r"z\s*=", r"log", r"ln", r"polynomial", r"quadratic", 
        r"remainder theorem", r"simultaneous", r"surds", r"indices", r"logarithms", r"partial fractions",
        r"real part", r"imaginary part", r"modulus", r"argument", r"conjugate", r"binary operation",
        r"equal roots", r"roots of the equation", r"divisible", r"remainder", r"cube root of unity",
        r"subsets", r"solve the equation", r"factorize", r"expression", r"thrice the other", r"twice the other",
        r"reciprocals", r"value of y", r"calculate cot"
    ],
    "Sequences, Series & Binomial Expansion": [
        r"\\sum", r"T_n", r"S_n", r"\\binom", r"arithmetic progression", 
        r"geometric progression", r"\\bAP\\b", r"\\bGP\\b", r"sum to infinity", r"binomial theorem", r"expansion",
        r"A\.P", r"term of an"
    ],
    "Trigonometry & Coordinate Geometry": [
        r"\\sin", r"\\cos", r"\\tan", r"\\theta", r"\\pi", r"sine rule", 
        r"cosine rule", r"elevation", r"depression", r"coordinate", r"gradient", r"circle theorem", r"locus",
        r"ellipse", r"foci", r"focus", r"tangent", r"circle", r"parabola", r"mid-point", r"straight line",
        r"perpendicular", r"slope", r"eccentricity", r"conic", r"parametric equations", r"triangle"
    ],
    "Calculus (Differentiation & Integration)": [
        r"\\int", r"\\frac{dy}{dx}", r"f'\(x\)", r"differentiation", r"derivative", 
        r"chain rule", r"product rule", r"quotient rule", r"integration", r"definite integral", r"maxima", r"minima",
        r"differentiate", r"first principle", r"integrate", r"differential equation", r"curve", r"rectangular enclosure", r"approximation",
        r"evaluate lim"
    ],
    "Vectors & Mechanics": [
        r"\\vec", r"\\mathbf", r"vector", r"scalar", r"magnitude", 
        r"dot product", r"cross product", r"resultant", r"relative velocity", r"statics", r"dynamics"
    ],
    "Statistics & Probability": [
        r"\\bar{x}", r"\\sigma", r"P\(A\)", r"mean", r"median", r"mode", 
        r"variance", r"standard deviation", r"cumulative frequency", r"permutation", r"combination", r"probability"
    ],
    "Matrices & Determinants": [
        r"\\begin\{pmatrix\}", r"\\begin\{matrix\}", r"\\det", r"matrix", 
        r"matrices", r"determinant", r"inverse", r"transpose", r"linear transformation"
    ]
}

# Comprehensive topic mapping rules for Physics
PHYSICS_TOPICS = {
    "Mechanics & Properties of Matter": [
        r"kinematics", r"acceleration", r"projectile", r"friction", r"momentum", 
        r"Newton", r"work", r"energy", r"power", r"simple harmonic motion", r"elasticity", r"Hooke", r"surface tension", r"viscosity",
        r"bullet", r"mass", r"penetrates", r"block of wood", r"fluid", r"flow velocity", r"pipe", r"pressure", r"reynold",
        r"u-tube", r"bulk modulus", r"rigidity", r"aeroplane", r"bomb", r"angular speed", r"tangential speed", r"pump",
        r"relative velocity", r"centripetal", r"bernoulli", r"terminal speed", r"equilibrium", r"horizontal range", r"maximum height",
        r"triangle law", r"parallelogram law", r"falling body", r"speed and velocity", r"coefficient of restitution", 
        r"c\.g", r"center of gravity", r"ball dropped", r"conservative forces"
    ],
    "Waves, Sound & Optics": [
        r"wave", r"transverse", r"longitudinal", r"resonance", r"Doppler", 
        r"refraction", r"reflection", r"lens", r"mirror", r"diffraction", r"interference", r"critical angle", r"optical fiber",
        r"whistle", r"frequency", r"overtone", r"harmonic", r"closed pipe", r"open pipe", r"prism", r"deviation",
        r"telescope", r"focal length", r"echo", r"sound", r"refractive index", r"angle of incidence", r"ray of light"
    ],
    "Thermal Physics & Thermodynamics": [
        r"heat capacity", r"latent heat", r"conduction", r"convection", r"radiation", 
        r"gas laws", r"Boyle", r"Charles", r"thermal expansion", r"thermodynamics",
        r"temperature", r"thermometer", r"solar constant", r"evaporation", r"cooling", r"adiabatic", r"isothermal", r"entropy",
        r"volume expansivity", r"linear expansivity", r"mercury level", r"first law of thermodynamic", r"thermodynamic processes"
    ],
    "Electricity & Magnetism": [
        r"Ohm", r"resistor", r"potentiometer", r"bridge", r"capacitance", 
        r"electric field", r"potential difference", r"magnetic flux", r"electromagnetic induction", r"transformer", r"alternating current", r"dynamo",
        r"current", r"magnetic field", r"wire", r"kirchhoff", r"branch", r"node", r"loop", r"monopole", r"impedance", r"reactance", r"battery", r"internal resistance",
        r"permeability", r"susceptibility", r"ammeter", r"voltmeter", r"rheostat", r"alternating voltage", r"equivalent inductance"
    ],
    "Fields (Gravitational, Electric & Magnetic)": [
        r"gravitational field", r"escape velocity", r"Coulomb", r"magnetic force", r"flux density",
        r"universal gravitation", r"mass of the earth", r"density of the earth", r"moon", r"electrostatic force"
    ],
    "Modern & Quantum Physics": [
        r"radioactivity", r"half-life", r"nuclear fission", r"fusion", 
        r"photoelectric", r"X-ray", r"energy levels", r"semiconductor", r"diode", r"transistor",
        r"disintegration", r"decay constant", r"carbon-14", r"cathode rays", r"alpha-particle", r"beta-particle",
        r"thermionic emission", r"field emission", r"emission of electron", r"planck's constant", r"excitation potential"
    ],
    "Practicals": [
        r"dimension", r"dimensional analysis", r"fundamental quantities", r"derived quantities",
        r"straight line graph", r"composite table", r"percentage error", r"slope", r"vander waal", r"vanderwaal",
        r"precautions taken", r"test tube", r"float vertically", r"lead shots", r"\bP3\b", r"error in calculating",
        r"graph", r"table", r"error"
    ]
}

def classify_question(text, topics_dict):
    for topic, patterns in topics_dict.items():
        for pattern in patterns:
            if re.search(pattern, text, re.IGNORECASE):
                return topic
    return "General / Uncategorized"

def process_folder(subject_name, topics_dict):
    folder_path = os.path.join("data", subject_name)
    if not os.path.exists(folder_path):
        print(f"Directory {folder_path} not found.")
        return

    for filename in os.listdir(folder_path):
        if filename.endswith(".json"):
            file_path = os.path.join(folder_path, filename)
            with open(file_path, "r", encoding="utf-8") as f:
                try:
                    questions = json.load(f)
                except Exception as e:
                    continue
            
            updated_count = 0
            for q in questions:
                q["topic"] = classify_question(q.get("question", ""), topics_dict)
                updated_count += 1
            
            with open(file_path, "w", encoding="utf-8") as f:
                json.dump(questions, f, indent=4, ensure_ascii=False)
            
            print(f"Successfully re-tagged {updated_count} questions in {subject_name}/{filename}")

if __name__ == "__main__":
    process_folder("Mathematics", MATH_TOPICS)
    process_folder("Physics", PHYSICS_TOPICS)
    print("All Mathematics and Physics files have been successfully re-tagged!")