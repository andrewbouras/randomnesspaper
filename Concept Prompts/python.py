from openai import OpenAI
import csv

client = OpenAI(api_key='API_Key')  # Replace with your actual API key

# Base prompt
base_prompt = """
Generate 7 high-quality, clinically relevant multiple-choice questions using the selected facts. Each question should be a detailed vignette-style question that requires application of knowledge. Include patient demographics, presenting symptoms, relevant medical history, and pertinent test results in each vignette. Provide 5 possible answer choices per question, listed in alphabetical order. The wrong answer choices should be plausible and require careful consideration. Questions should test understanding, application, analysis, or evaluation of the concepts. After each question, include the correct answer choice and a brief explanation.
"""

# LCG parameters
seed = 12345
a = 1103515245
c = 12345
m = 2**31

# Initialize used facts
used_facts = set()

# Mapping of fact indices to descriptions
fact_mapping = {
    1: "Inheritance of Congenital Duodenal Atresia & Stenosis: Autosomal recessive.",
    2: "Association of Congenital Duodenal Atresia & Stenosis: Down Syndrome.",
    3: "Pathology of Congenital Duodenal Atresia & Stenosis: Failure of canalization of the embryonic duodenum.",
    4: "Prenatal Signs of Congenital Duodenal Atresia & Stenosis: Difficulty swallowing & absorption of amniotic fluid.",
    5: "Postnatal Signs of Congenital Duodenal Atresia & Stenosis: Bilious & nonbilious vomiting.",
    6: "Type 1 Congenital Duodenal Atresia: Septum within the bowel.",
    7: "Type 2 Congenital Duodenal Atresia: Gap in the bowel, connected by a fibrous cord.",
    8: "Type 3 Congenital Duodenal Atresia (Apple peel/Christmas tree): Affects jejunum, mal-rotated intestine, absent mesenteric arteries.",
    9: "Pathology of Meckel's Diverticulum: Failure of involution of the omphalomesenteric (vitelline) duct.",
    10: "Histology of Meckel's Diverticulum: True diverticulum with all 3 bowel layers, contains heterotopic mucosa (gastric, colonic, pancreatic).",
    11: "Rule of 2 for Meckel's Diverticulum: 2% of infants, 2 feet from ileocecal valve, 2 inches long.",
    12: "Ectopic Mucosa in Meckel's Diverticulum: Gastric & pancreatic; can lead to vitamin B12 deficiency.",
    13: "Pathology of Meconium Ileus: Bowel obstruction due to thick & sticky meconium.",
    14: "Association of Meconium Ileus: Neonates with cystic fibrosis.",
    15: "Gross Pathology of Meconium Ileus: Proximal bowel ischemic & dilated, obstruction & impaired motility.",
    16: "General Effects of Meconium Ileus: Accumulated thickened meconium.",
    17: "Histology of Meconium Ileus: Normal villi, abnormal brush border mucosal enzymes.",
    18: "Signs of Meconium Ileus: Failure to pass meconium in the first 12-24 hours.",
    19: "Pathology of Shiga Toxin & Mediated Thrombotic Microangiopathy: Hemolytic anemia, thrombocytopenia, renal failure, schistocytes, decreased haptoglobin.",
    20: "Association of Shiga Toxin & Mediated Thrombotic Microangiopathy: E. coli strain O157:H7.",
    21: "Toxin Cytotoxicity in Shiga Toxin: Activation of complement pathways, endothelial damage.",
    22: "Glomerular Effects of Shiga Toxin: Capillary thromboses, widened subendothelial space, congested glomeruli, necrosis of capillary walls.",
    23: "Pathogenesis of Inflammatory Bowel Disease (IBD): Failure to downregulate, T cell activation, leukocyte trafficking to the colon, cytokine secretion, increased intestinal permeability.",
    24: "Key Points of Ulcerative Colitis (UC): Continuous superficial inflammation, colon only, variable extent.",
    25: "Locations of Ulcerative Colitis: Rectum only (25%), rectosigmoid (50%), extensive colitis (25%), pancolitis (entire colon).",
    26: "Gross Appearance of Ulcerative Colitis: Granularity, spontaneous hemorrhage, mucopus, ulcerations, pseudopolyps.",
    27: "Histology of Ulcerative Colitis: Crypt lumen with polymorphic neutrophils, crypt abscesses, superficial ulcerations.",
    28: "Clinical Manifestations of Ulcerative Colitis: Rectal bleeding, tenesmus, diarrhea, abdominal cramping, mucopus.",
    29: "Laboratory Abnormalities in Ulcerative Colitis: Iron deficiency anemia, elevated ESR, CRP, LFTs, decreased albumin.",
    30: "Chronic Changes in Ulcerative Colitis: Loss of haustrations, thickening of smooth muscle, dysplasia, adenocarcinoma.",
    31: "Key Points of Crohn's Disease: Patchy full-thickness inflammation, mouth to anus involvement, fistulas & strictures.",
    32: "Common Location of Crohn's Disease: Terminal ileum & right colon, skip lesions, segmental distribution.",
    33: "Gross Endoscopic Appearance of Crohn's Disease: Ulcerations, 'cobblestone' mucosa.",
    34: "Microscopic Appearance of Crohn's Disease: Non-caseating granulomas.",
    35: "Clinical Manifestations of Crohn's Disease: Abdominal cramping & tenderness, mass on physical exam, diarrhea, perianal disease.",
    36: "Lab Values in Crohn's Disease: Iron deficiency anemia, elevated ESR, CRP, decreased folic acid, vitamin B12, total protein.",
    37: "Diagnosis of Crohn's Disease: Requires the entire clinical picture, no single pathognomonic feature.",
    38: "Special Tests for Crohn's Disease: Endoscopic examinations (colonoscopy, upper endoscopy, enteroscopy, capsule endoscopy), radiological examinations (barium enemas, small bowel series, CT & MRI).",
    39: "Goals in Treating IBD: Confirm accurate diagnosis, induce & maintain remission, enhance quality of life, avoid adverse effects.",
    40: "Drug Therapies for IBD: Aminosalicylates, corticosteroids, immunomodulators, antibiotics, supportive agents.",
    41: "Overview of Irritable Bowel Syndrome (IBS): Chronic abdominal pain, change in bowel habits, more prevalent in females.",
    42: "Pathology of IBS: Dysregulation of ANS & ENS, gut microbiome changes.",
    43: "Rome IV Diagnostic Criteria for IBS: Recurrent abdominal pain (at least 1 day/week for 3 months), associated with defecation, change in stool frequency, change in stool form.",
    44: "Types of IBS: IBS-C (Type 1 & 2 stools > 25% of the time), IBS-D (Type 6 & 7 stools > 25% of the time), IBS-M (mixed stools > 25% of the time).",
    45: "Symptoms of IBS: Abdominal pain (waxes/wanes, nocturnal pain uncommon), bloating, mucorrhea.",
    46: "Alarm Features NOT consistent with IBS: Hematochezia, weight loss, occult + / FIT +, vomiting, age > 45.",
    47: "Treatment for IBS: Low-FODMAP diet, consider Celiac disease.",
    48: "Maldigestion: Impaired digestion of nutrients within the intestinal lumen, exocrine pancreatic insufficiency, lactose maldigestion.",
    49: "Malabsorption: Impaired absorption of dietary nutrients.",
    50: "Global Malabsorption: Example: Celiac disease.",
    51: "Selective Malabsorption: Example: Pernicious anemia leading to vitamin B12 malabsorption.",
    52: "Primary (Congenital) Malabsorption.",
    53: "Acquired Malabsorption: Example: Crohn's disease, Celiac disease, surgeries.",
    54: "Fat Malabsorption: Pale & voluminous stool, diarrhea without flatulence, steatorrhea.",
    55: "Protein Malabsorption: Edema, muscle atrophy, amenorrhea.",
    56: "Carb Malabsorption: Watery diarrhea, flatulence, acidic stool pH, milk intolerance.",
    57: "Celiac Disease: Immune-mediated enteropathy triggered by gluten, presents with dermatitis herpetiformis, positive tTG, endomysial antibody, and deamidated gliadin.",
    58: "Iron & Iron Deficiency Absorption: Maximal absorption at the duodenum.",
    59: "Folic Acid Deficiency: Macrocytic anemia, glossitis, oral ulcers.",
    60: "Lipophilic Vitamin Absorption: ADEK.",
    61: "Vitamin B12 Deficiency: High MMA & homocysteine.",
    62: "Vitamin A Deficiency: Night blindness, xerophthalmia, keratomalacia, Bitot spot, follicular hyperkeratosis.",
    63: "Vitamin E Deficiency: Ataxia, hyporeflexia, loss of proprioceptive & vibratory sensation.",
    64: "Vitamin K Deficiency: Impaired coagulation, bruising, mucosal bleeding, splinter hemorrhages, melena, hematuria, elevated PT & PTT.",
    65: "Benign Tumors of the Small Intestine: Lipomas (ileum > jejunum), leiomyomas (MC benign tumor).",
    66: "Malignant Tumors of the Small Intestine: Carcinoid (MC), adenocarcinoma, lymphoma, leiomyosarcoma.",
    67: "SBO Etiology: Adhesions (60%), hernia (20%), neoplasm, volvulus.",
    68: "LBO Etiology: Cancer (60%), diverticular disease, volvulus.",
    69: "SBO Complications: Electrolyte imbalance, dehydration, bowel wall edema.",
    70: "SBO Diagnosis: Abdominal distention & pain, x-rays, small bowel series, CT scan.",
    71: "SBO Risk: Ischemia/Infarction.",
    72: "Diverticulosis: Diverticula (outpouchings) present without inflammation.",
    73: "Diverticulitis: Inflammation of diverticula.",
    74: "Diverticulitis Treatment: Mostly medical, surgical for complicated or recurrent disease.",
    75: "Colonic Obstruction: MCC is adenocarcinoma, treated with surgery.",
    76: "Colon Carcinoma: Metachronous vs synchronous, MC metastasis to regional lymph nodes & liver.",
    77: "Colon Carcinoma Treatment: Surgical resection.",
    78: "Colostomy Terminology: Colostomy, Hartmann's procedure, loop colostomy, colocolostomy, right hemicolectomy.",
    79: "Volvulus Pathology: Twisting of intestines upon itself ('bird beak sign').",
    80: "Volvulus Location: Sigmoid (70%), cecal (30%).",
    81: "Volvulus Diagnosis: Barium enema, sigmoidoscopy.",
    82: "Volvulus Treatment: Colonoscopy, then surgical (resection indicated if mucosa is ischemic).",
    83: "Intussusception Pathology: One portion of intestine telescopes into another.",
    84: "Intussusception Treatment: Surgical intervention due to high incidence of malignancy.",
    85: "Anal Canal Anatomy: ~ 3 cm, from anal verge to dentate/pectinate line, lined by squamous epithelium, contains somatic sensory nerves (responds to pain).",
    86: "Dentate Line: Junction between columnar epithelium & the anoderm.",
    87: "Columns of Morgagni: Longitudinal folds proximal to the dentate line.",
    88: "Anal Crypts: Secrete anal glands, site of origin for perirectal abscesses.",
    89: "Venous Drainage of Anoderm vs Rectum: Anoderm: Caval (IVC) system; Rectum: Portal system.",
    90: "Hemorrhoidal Plexus: Connects caval & portal system, distention & enlargement can lead to hemorrhoids.",
    91: "Defecation Process: Bolus distends upper rectum, autonomic sensory nerve sends signal to spinal cord, proximal colon contracts, internal anal sphincter relaxes.",
    92: "Internal Hemorrhoids: Above dentate line, covered by insensitive rectal mucosa.",
    93: "External Hemorrhoids: Below dentate line, covered by sensitive anoderm.",
    94: "Symptoms of Internal Hemorrhoids: Discomfort (not pain), bleeding, prolapse.",
    95: "Symptoms of External Hemorrhoids: Severe pain, thrombosis.",
    96: "Location of Perianal Abscesses: Infalevator (common), perianal, ischiorectal, postanal, supralevator (rare).",
    97: "Hemorrhoid Therapies: Sclerotherapy, cryotherapy, dietary manipulation, banding, surgical hemorrhoidectomy.",
    98: "Conservative Hemorrhoid Treatment: Stool softeners, bulking agents, sitz baths, topical anesthetics.",
    99: "Internal Hemorrhoid Treatment: Rubber band ligation.",
    100: "Stage 3 Prolapsing Hemorrhoid Treatment: Excision (closed hemorrhoidectomy preferred)."
}


def lcg(seed, a, c, m):
    """Linear Congruential Generator."""
    while True:
        seed = (a * seed + c) % m
        yield seed % 100 + 1

# Initialize LCG
lcg_generator = lcg(seed, a, c, m)

def get_unique_facts(used_facts, fact_mapping, lcg_generator):
    """Get a list of unique facts that haven't been used."""
    unique_facts = []
    while len(unique_facts) < 7:
        fact_id = next(lcg_generator)
        if fact_id not in used_facts and fact_id in fact_mapping:
            unique_facts.append(fact_id)
            used_facts.add(fact_id)
    return unique_facts

def generate_mcqs(facts, base_prompt, fact_mapping):
    """Generate MCQs based on selected facts."""
    facts_text = "\n".join([f"{fact_mapping[fact_id]}" for fact_id in facts])
    
    method_prompt = f"""Using the Linear Congruential Generator (LCG) method with seed 12346, 
    a list of random numbers within the range of 1-100 was generated. 
    These numbers are unique and have not been used in previous rounds. 
    The generated numbers are: {facts}. 
    Use these random numbers to select corresponding facts from the provided list 
    and create unique multiple-choice questions (MCQs) related to gastrointestinal physiology."""
    
    full_prompt = f"{facts_text}\n\n{method_prompt}\n\n{base_prompt}"
    
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": full_prompt}
        ],
        max_tokens=1500
    )
    
    return response.choices[0].message.content.strip()

# Main loop
rounds = 14
summary = []

for i in range(rounds):
    print(f"Round {i + 1}")
    unique_facts = get_unique_facts(used_facts, fact_mapping, lcg_generator)
    mcqs = generate_mcqs(unique_facts, base_prompt, fact_mapping)
    summary.append([i + 1, "LCG", "Unique", mcqs, unique_facts])
    print(f"Round {i + 1} MCQs:\n{mcqs}\n")
    print(f"Used Facts in Round {i + 1}: {unique_facts}\n")

output_file = 'mcq_generation_summary_lcg.csv'
with open(output_file, 'w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(["Round", "Method", "Repeat Status", "MCQs", "Used Facts"])
    writer.writerows(summary)

print(f"Summary of MCQ generation saved to '{output_file}'")

# Compare facts between rounds to check for overlap
for i in range(len(summary) - 1):
    for j in range(i + 1, len(summary)):
        overlap = set(summary[i][4]).intersection(set(summary[j][4]))
        if overlap:
            print(f"Overlap of facts between round {summary[i][0]} and round {summary[j][0]}: {overlap}")
        else:
            print(f"No overlap between round {summary[i][0]} and round {summary[j][0]}")