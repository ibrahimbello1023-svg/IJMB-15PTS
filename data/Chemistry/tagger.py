import json
import os
import re

# Define your topics and keywords
TOPIC_KEYWORDS = {
    "Electrochemistry": [
        "electrochemical",
        "electrolytic",
        "electrode",
        "emf",
        "cathode",
        "anode",
        "cell",
        "electrolysis",
    ],
    "Organic Chemistry": [
        "alkane",
        "alkene",
        "alkyne",
        "isomer",
        "functional group",
        "saponification",
        "esterification",
        "decarboxylation",
        "ethanamide",
        "propanal",
        "decane",
    ],
    "Chemical Equilibrium": [
        "equilibrium",
        "kc",
        "kp",
        "dissociation",
        "le chatelier",
    ],
    "Periodic Table & Periodicity": [
        "atomic radius",
        "ionic radius",
        "ionisation energy",
        "s-block",
        "p-block",
        "d-block",
        "periodic table",
        "isotopy",
    ],
    "Stoichiometry & Volumetric Analysis": [
        "titration",
        "mole",
        "concentration",
        "titre",
        "standard solution",
        "purity",
        "pipette",
    ],
    "States of Matter & Gas Laws": [
        "diffusion",
        "victor meyer",
        "vapour pressure",
        "density",
        "gas",
    ],
    "Inorganic & Coordination Chemistry": [
        "coordination number",
        "ligand",
        "isomerism",
        "complex ion",
        "transition metals",
        "aluminium",
    ],
}


def assign_topic(question_text):
  text_lower = question_text.lower()
  for topic, keywords in TOPIC_KEYWORDS.items():
    for keyword in keywords:
      if re.search(r"\b" + re.escape(keyword) + r"\b", text_lower):
        return topic
  return "General Chemistry"


def tag_all_chemistry_files():
  folder_path = "."

  # Check if folder exists
  if not os.path.exists(folder_path):
    print(f"Error: Folder '{folder_path}' not found.")
    return

  # Loop through every file in the folder
  for filename in os.listdir(folder_path):
    if filename.endswith(".json") and filename != "tagger.py":
      file_path = os.path.join(folder_path, filename)

      with open(file_path, "r", encoding="utf-8") as f:
        try:
          questions = json.load(f)
        except json.JSONDecodeError:
          print(f"Skipping {filename} (not valid JSON)")
          continue

      updated = False
      for q in questions:
        q_text = q.get("question", "") or q.get("text", "")
        if "topic" not in q or not q["topic"]:
          q["topic"] = assign_topic(q_text)
          updated = True

      with open(file_path, "w", encoding="utf-8") as f:
        json.dump(questions, f, indent=4)

      print(f"Successfully tagged: {filename}")


if __name__ == "__main__":
  tag_all_chemistry_files()