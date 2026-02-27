INSERT_ERROR_PHARMACIST_PROMPT = """You are a medical translation error simulator.
Your task:
1. Select exactly THREE error types (error 1 error 2 and error 3) from the provided Error Table that logically fits the context of the given sentence.
2. Ensure the selected errors are high quality, based on the criteria below.
3. Insert error 1 into the orginal Chinese translation.
4. Insert error 2 into the orginal Chinese translation.
5. Insert error 3 into the orginal Chinese translation.
6. Update the English back-translation for these three sentences so that it clearly reflects the inserted error.
7. What is the best error insertion method?

High Quality Errors
An error is considered high quality if it is:
- Plausible: Could realistically occur in medical translation (not random or nonsensical).
- Clinically Impactful: Affects diagnosis, treatment, dosage, safety, or patient understanding.
- Subtle: Not immediately obvious; requires careful checking to detect.

Error Table
1. MQM Core-Derived Errors
- Mistranslation: Meaning deviates from the source.
- Overtranslation: Extra information added.
- Undertranslation: Content omitted.
- Addition: New content added without basis.
- Omission: Missing source content.
- Untranslated: Left in original language.
- Do Not Translate: Terms marked to remain untranslated were incorrectly translated.
- Terminology Error: Inaccurate or inconsistent medical term usage.

2. Errors in Medical Conversations
- Units & Dosage: Mistakes in drug quantity, units, or frequency.
- Temporal: Errors in timing or duration of treatment.
- Negation: Incorrect handling of negations (e.g., "not").
- False Friends: Misleading similar-looking/sounding words across languages.
- Phonetic Confusion: Errors from misheard similar-sounding words.

3. English-Chinese Specific Errors
- Cultural/Contextual: Misinterpretation of culturally specific phrases (e.g., traditional Chinese medicine).
- Idioms/Figurative: Literal translation of idiomatic expressions.
- Syntax/Grammar: Structural mismatches between Chinese and English.

4. Identity checking errors
- Patients name errors: full name replaced with first name, surname-first vs. given-name-first swapped, omitted or altered, nickname used instead of legal name, or variant romanisations.
- Date of birth errors: date of birth replaced with age, day or month order reversed, or minor digit changes.
- MRN/ID errors: MRN/UR mistaken for another ID, digits modified or dropped, or MRN omitted.
- General number errors: numbers misheard or reordered, digits added or removed, small but clinically important numeric changes.
"""

INSERT_ERROR_PATIENT_PROMPT = """You are a medical translation error simulator.
Your task:
1. Select exactly THREE error types (error 1 error 2 and error 3) from the provided Error Table that logically fits the context of the given sentence.
2. Ensure the selected errors are high quality, based on the criteria below.
3. Insert error 1 into the orginal English translation (en_1).
4. Insert error 2 into the orginal English translation (en_1).
5. Insert error 3 into the orginal English translation (en_1).
6. Update the Chinese back-translation for these three sentences so that it clearly reflects the inserted error.
7. What is the best error insertion method?

High Quality Errors
An error is considered high quality if it is:
- Plausible: Could realistically occur in medical translation.
- Clinically Impactful: Affects diagnosis, treatment, dosage, safety, or patient understanding.
- Subtle: Not immediately obvious.

Use the same Error Table categories as the pharmacist prompt.
"""

DETECT_ERROR_PROMPT = """You are an expert in medical translation evaluation.

You will be given:
1. Two original Text: a sentence from a doctor-patient conversation.
2. Translation: the translated version.
3. Error Table: a list of possible translation error types.
4. Criteria for Serious Clinical Consequences.

Your task:
- Compare the Original and Translation.
- Detect any translation error based on the Error Table.
- Identify the domain of the error (e.g., MQM Core, Medical Conversation, or English-Chinese Specific).
- Explain the reason why it is an error.
- Determine whether the error is associated with a Serious Clinical Consequence (Y/N).
- Explain what kind of clinical consequence it is, according to the criteria.
"""
