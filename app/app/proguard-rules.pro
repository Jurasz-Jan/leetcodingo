# Reguły R8 dla buildu release.
#
# kotlinx.serialization dostarcza własne reguły w bibliotece, więc klasy z
# @Serializable nie wymagają tu wpisów. Poniższe dwie rzeczy są jednak nasze.

# Nazwy pól modelu są kontraktem z korpusem, nie szczegółem implementacji:
# gdyby R8 je przemianował, deserializacja JSON-a przestałaby trafiać w pola.
-keepclassmembers class pl.leetcodingo.data.** {
    <fields>;
}

# Czytelne ślady stosu w raportach z urządzenia.
-keepattributes SourceFile,LineNumberTable
-renamesourcefileattribute SourceFile
