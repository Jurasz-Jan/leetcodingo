package pl.leetcodingo.data

import android.content.Context
import android.util.Log
import java.io.File

data class Corpus(
    val patterns: List<PatternMeta>,
    val exercises: List<Exercise>,
    val skipped: Int,
    val origin: String,
)

/**
 * Czyta korpus, najpierw z katalogu na urzadzeniu, a dopiero potem z assetow.
 *
 * Assety sa zapasem i wersja, ktora jedzie w APK. Katalog na urzadzeniu istnieje po to,
 * zeby praca nad trescia nie wymagala budowania aplikacji: korpus zmienia sie dziesiec
 * razy czesciej niz kod, a `adb push` trwa sekunde zamiast minut.
 *
 *     python generator/build.py
 *     adb push corpus/. /sdcard/Android/data/pl.leetcodingo/files/corpus/
 *
 * To katalog przypisany do aplikacji, wiec nie wymaga zadnego uprawnienia i znika razem
 * z odinstalowaniem. Pusty albo nieistniejacy katalog oznacza po prostu powrot do
 * assetow, wiec na cudzym telefonie ta sciezka jest niewidoczna.
 */
class CorpusRepository(private val context: Context) {

    fun load(): Corpus {
        val fromDevice = deviceFiles()
        return if (fromDevice.isNotEmpty()) {
            Log.i(TAG, "korpus z urzadzenia: ${fromDevice.size} plikow")
            parse(fromDevice.map { it.name to it.readText() }, origin = "urządzenie")
        } else {
            val names = context.assets.list(DIR).orEmpty().filter { it.endsWith(".json") }.sorted()
            parse(names.map { name -> name to readAsset(name) }, origin = "assety")
        }
    }

    private fun deviceFiles(): List<File> =
        context.getExternalFilesDir(DIR)
            ?.listFiles { file -> file.isFile && file.name.endsWith(".json") }
            ?.sortedBy { it.name }
            .orEmpty()

    private fun readAsset(name: String): String =
        context.assets.open("$DIR/$name").bufferedReader().use { it.readText() }

    private fun parse(files: List<Pair<String, String>>, origin: String): Corpus {
        val patterns = mutableListOf<PatternMeta>()
        val exercises = mutableListOf<Exercise>()
        var skipped = 0

        for ((name, raw) in files) {
            val file = runCatching { corpusJson.decodeFromString<CorpusFile>(raw) }.getOrElse {
                // Uszkodzony plik wgrany na urzadzenie nie moze wywrocic calej sesji.
                Log.w(TAG, "pomijam $name: ${it.message}")
                continue
            }
            patterns += file.pattern
            for (dto in file.exercises) {
                val exercise = dto.toExerciseOrNull()
                if (exercise == null) skipped++ else exercises += exercise
            }
        }
        return Corpus(patterns = patterns, exercises = exercises, skipped = skipped, origin = origin)
    }

    private companion object {
        const val DIR = "corpus"
        const val TAG = "leetcodingo"
    }
}
