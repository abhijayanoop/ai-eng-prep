from __future__ import annotations
import tiktoken

passages: dict[str, str] = {
    "English": """
    Welcome to the food delivery service. You can use this assistant to
    check the status of an order, understand an estimated delivery time,
    report a missing item, or ask for help with a payment. When you place
    an order, the restaurant first confirms it and starts preparing your
    food. A delivery partner is then assigned to collect the package and
    bring it to your location. The estimated arrival time can change
    because of traffic, weather, restaurant preparation time, or other
    unexpected delays. If your order appears to be delayed, check the
    latest status before contacting support. If an item is missing or
    incorrect, keep the order details ready so the support team can
    identify the problem. Never share your password or one-time
    authentication code with anyone. Use the official application to
    manage your address, payment options, and order history. Clear
    communication helps the support assistant provide a useful answer.
    """,
    "Hindi": """
    खाद्य वितरण सेवा में आपका स्वागत है। आप इस सहायक का उपयोग अपने
    ऑर्डर की स्थिति जानने, अनुमानित डिलीवरी समय समझने, किसी गायब वस्तु
    की सूचना देने या भुगतान से जुड़ी सहायता माँगने के लिए कर सकते हैं।
    ऑर्डर देने के बाद रेस्तराँ पहले उसकी पुष्टि करता है और भोजन तैयार
    करना शुरू करता है। इसके बाद भोजन लेने और आपके पते तक पहुँचाने के
    लिए डिलीवरी पार्टनर नियुक्त किया जाता है। ट्रैफ़िक, मौसम, भोजन
    तैयार होने में लगने वाले समय या अन्य अप्रत्याशित कारणों से पहुँचने
    का अनुमानित समय बदल सकता है। यदि ऑर्डर में देरी दिखाई दे, तो
    सहायता से संपर्क करने से पहले नवीनतम स्थिति जाँचें। यदि कोई वस्तु
    गायब है या गलत है, तो ऑर्डर का विवरण तैयार रखें ताकि सहायता टीम
    समस्या पहचान सके। अपना पासवर्ड या एक बार उपयोग होने वाला
    प्रमाणीकरण कोड किसी के साथ साझा न करें। अपना पता, भुगतान विकल्प
    और ऑर्डर इतिहास प्रबंधित करने के लिए आधिकारिक ऐप का उपयोग करें।
    स्पष्ट जानकारी से सहायता सहायक आपको उपयोगी उत्तर दे सकता है।
    """,
    "Malayalam": """
    ഭക്ഷണ വിതരണ സേവനത്തിലേക്ക് സ്വാഗതം. ഓർഡറിന്റെ നില പരിശോധിക്കാനും
    പ്രതീക്ഷിക്കുന്ന ഡെലിവറി സമയം മനസ്സിലാക്കാനും കാണാതായ സാധനത്തെക്കുറിച്ച്
    അറിയിക്കാനും പണമടയ്ക്കലുമായി ബന്ധപ്പെട്ട സഹായം തേടാനും നിങ്ങൾക്ക്
    ഈ സഹായിയെ ഉപയോഗിക്കാം. നിങ്ങൾ ഓർഡർ നൽകിയാൽ റെസ്റ്റോറന്റ് ആദ്യം
    അത് സ്ഥിരീകരിക്കുകയും ഭക്ഷണം തയ്യാറാക്കാൻ തുടങ്ങുകയും ചെയ്യും.
    തുടർന്ന് ഭക്ഷണം ഏറ്റുവാങ്ങി നിങ്ങളുടെ വിലാസത്തിലെത്തിക്കാൻ ഒരു
    ഡെലിവറി പങ്കാളിയെ നിയോഗിക്കും. ഗതാഗതക്കുരുക്ക്, കാലാവസ്ഥ, ഭക്ഷണം
    തയ്യാറാക്കാൻ വേണ്ട സമയം, മറ്റ് അപ്രതീക്ഷിത കാരണങ്ങൾ എന്നിവ കാരണം
    എത്തിച്ചേരാനുള്ള ഏകദേശ സമയം മാറാം. ഓർഡർ വൈകുന്നതായി തോന്നിയാൽ
    സഹായവുമായി ബന്ധപ്പെടുന്നതിന് മുമ്പ് ഏറ്റവും പുതിയ നില പരിശോധിക്കുക.
    ഏതെങ്കിലും സാധനം കാണാതാകുകയോ തെറ്റായ സാധനം ലഭിക്കുകയോ ചെയ്താൽ
    പ്രശ്നം തിരിച്ചറിയാൻ സഹായിക്കുന്നതിനായി ഓർഡർ വിവരങ്ങൾ തയ്യാറാക്കി
    വയ്ക്കുക. നിങ്ങളുടെ പാസ്‌വേഡോ ഒറ്റത്തവണ ഉപയോഗിക്കുന്ന സുരക്ഷാ
    കോഡോ ആരുമായും പങ്കിടരുത്. വിലാസം, പണമടയ്ക്കൽ മാർഗങ്ങൾ, ഓർഡർ
    ചരിത്രം എന്നിവ കൈകാര്യം ചെയ്യാൻ ഔദ്യോഗിക ആപ്പ് ഉപയോഗിക്കുക.
    വ്യക്തമായ വിവരങ്ങൾ നൽകുന്നത് സഹായിക്ക് പ്രയോജനകരമായ മറുപടി
    നൽകാൻ സഹായിക്കും.
    """,
}

ENCODING_NAME = "cl100k_base"
encoding = tiktoken.get_encoding(ENCODING_NAME)

def count_words(text: str) -> int:
    return len(text.split());

def count_tokens(text: str) -> int:
    return len(encoding.encode(text))

def analyze_text(text: str) -> dict[str, int|float]:
    words = count_words(text)
    tokens = count_tokens(text)
    tokens_per_word = tokens/words if words>0 else 0.0

    return {
        "total_words": words,
        "token_count": tokens,
        "token_per_word": tokens_per_word
    }

def main() -> None:
    results: dict[str, dict[str, int | float]] = {}

    for language, passage in passages.items():
        results[language] = analyze_text(passage)

    english_ratio = results["English"]["token_per_word"]

    print(f"Encoding: {ENCODING_NAME}")
    print(
        f"{'Language':<12}"
        f"{'Words':>10}"
        f"{'Tokens':>10}"
        f"{'Tokens/word':>15}"
        f"{'Ratio vs EN':>15}"
    )
    print("-" * 62)

    for language, result in results.items():
        tokens_per_word = float(result["token_per_word"])
        relative_ratio = (
            tokens_per_word / english_ratio if english_ratio > 0 else 0.0
        )
        print(
            f"{language:<12}"
            f"{int(result['total_words']):>10}"
            f"{int(result['token_count']):>10}"
            f"{tokens_per_word:>15.3f}"
            f"{relative_ratio:>15.3f}"
        )

    requests_per_language = 1_000_000
    print(
        f"\\nIllustrative input tokens per {requests_per_language:,} "
        "requests (user passage only):"
    )
    for language, result in results.items():
        total = int(result["token_count"]) * requests_per_language
        print(f"{language:<12}{total:>18,}")

if __name__ == "__main__":
    main()
