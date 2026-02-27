import dspy

from .prompts import (
    DETECT_ERROR_PROMPT,
    INSERT_ERROR_PATIENT_PROMPT,
    INSERT_ERROR_PHARMACIST_PROMPT,
)


class InsertErrorPharmacist(dspy.Signature):
    __doc__ = INSERT_ERROR_PHARMACIST_PROMPT

    en_1 = dspy.InputField(desc="Original English text of the conversation turn")
    cn_1 = dspy.InputField(desc="Original accurate Chinese translation")

    errors_1 = dspy.OutputField(desc="Error category for error 1")
    errors_domain_1 = dspy.OutputField(desc="Which domain the error 1 belongs to")
    errors_explain_1 = dspy.OutputField(desc="Explanation for error 1")
    en_2_1 = dspy.OutputField(desc="English back-translation after error 1")
    cn_2_1 = dspy.OutputField(desc="Chinese translation with error 1 inserted")

    errors_2 = dspy.OutputField(desc="Error category for error 2")
    errors_domain_2 = dspy.OutputField(desc="Which domain the error 2 belongs to")
    errors_explain_2 = dspy.OutputField(desc="Explanation for error 2")
    en_2_2 = dspy.OutputField(desc="English back-translation after error 2")
    cn_2_2 = dspy.OutputField(desc="Chinese translation with error 2 inserted")

    errors_3 = dspy.OutputField(desc="Error category for error 3")
    errors_domain_3 = dspy.OutputField(desc="Which domain the error 3 belongs to")
    errors_explain_3 = dspy.OutputField(desc="Explanation for error 3")
    en_2_3 = dspy.OutputField(desc="English back-translation after error 3")
    cn_2_3 = dspy.OutputField(desc="Chinese translation with error 3 inserted")

    error_best = dspy.OutputField(desc="The best error insertion method")
    error_best_explain = dspy.OutputField(desc="Explanation of the best insertion method")
    ambiguity = dspy.OutputField(desc="Ambiguity feedback")


class InsertErrorPatient(dspy.Signature):
    __doc__ = INSERT_ERROR_PATIENT_PROMPT

    en_1 = dspy.InputField(desc="Original English text of the conversation turn")
    cn_1 = dspy.InputField(desc="Original accurate Chinese translation")

    errors_1 = dspy.OutputField(desc="Error category for error 1")
    errors_domain_1 = dspy.OutputField(desc="Which domain the error 1 belongs to")
    errors_explain_1 = dspy.OutputField(desc="Explanation for error 1")
    en_2_1 = dspy.OutputField(desc="English translation after error 1")
    cn_2_1 = dspy.OutputField(desc="Chinese back-translation with error 1")

    errors_2 = dspy.OutputField(desc="Error category for error 2")
    errors_domain_2 = dspy.OutputField(desc="Which domain the error 2 belongs to")
    errors_explain_2 = dspy.OutputField(desc="Explanation for error 2")
    en_2_2 = dspy.OutputField(desc="English translation after error 2")
    cn_2_2 = dspy.OutputField(desc="Chinese back-translation with error 2")

    errors_3 = dspy.OutputField(desc="Error category for error 3")
    errors_domain_3 = dspy.OutputField(desc="Which domain the error 3 belongs to")
    errors_explain_3 = dspy.OutputField(desc="Explanation for error 3")
    en_2_3 = dspy.OutputField(desc="English translation after error 3")
    cn_2_3 = dspy.OutputField(desc="Chinese back-translation with error 3")

    error_best = dspy.OutputField(desc="The best error insertion method")
    error_best_explain = dspy.OutputField(desc="Explanation of the best insertion method")
    ambiguity = dspy.OutputField(desc="Ambiguity feedback")


class DetectError(dspy.Signature):
    __doc__ = DETECT_ERROR_PROMPT

    en_1 = dspy.InputField(desc="Original text 1")
    cn_2_1 = dspy.InputField(desc="Translated text 1")
    cn_1 = dspy.InputField(desc="Original text 2")
    en_2_1 = dspy.InputField(desc="Translated text 2")

    errors_detected_text1 = dspy.OutputField(desc="Detected error type for text 1")
    errors_detected_domain_text1 = dspy.OutputField(desc="Detected error domain for text 1")
    errors_detected_domain_explain_text1 = dspy.OutputField(desc="Explanation for text 1")
    clinical_consequences_explain_text1 = dspy.OutputField(
        desc="Clinical consequence explanation for text 1"
    )
    clinical_consequences_flag_text1 = dspy.OutputField(
        desc="Clinical consequence flag for text 1"
    )

    errors_detected_text2 = dspy.OutputField(desc="Detected error type for text 2")
    errors_detected_domain_text2 = dspy.OutputField(desc="Detected error domain for text 2")
    errors_detected_domain_explain_text2 = dspy.OutputField(desc="Explanation for text 2")
    clinical_consequences_explain_text2 = dspy.OutputField(
        desc="Clinical consequence explanation for text 2"
    )
    clinical_consequences_flag_text2 = dspy.OutputField(
        desc="Clinical consequence flag for text 2"
    )
    ambiguity = dspy.OutputField(desc="Ambiguity feedback")
