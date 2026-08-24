import java.util.Properties

plugins {
    alias(libs.plugins.android.application)
    alias(libs.plugins.kotlin.android)
    alias(libs.plugins.kotlin.compose)
    alias(libs.plugins.kotlin.serialization)
}

/**
 * Korpus wjezdza do APK jako assety kopiowane z `corpus/` przy kazdym buildzie.
 * Renderer nie zawiera tresci na sztywno - przebudowa korpusu nie dotyka kodu.
 */
val copyCorpus by tasks.registering(Sync::class) {
    from(rootProject.file("../corpus")) { include("*.json") }
    into(layout.buildDirectory.dir("generated/corpus/corpus"))
}

/**
 * Dane klucza podpisujacego. Nigdy nie trafiaja do repozytorium.
 *
 * Kolejnosc: plik `keystore.properties` obok `settings.gradle.kts`, a jesli go nie ma,
 * zmienne srodowiskowe - tak dziala to samo w CI, gdzie klucz przychodzi z sekretow.
 * Gdy nie ma ani jednego, ani drugiego, build `release` podpisuje sie kluczem
 * debugowym: nie wywala sie, ale takie APK nie nadaje sie do rozdawania, bo klucz
 * debugowy jest przywiazany do maszyny.
 */
val keystoreProperties = Properties()
val keystorePropertiesFile = rootProject.file("keystore.properties")
if (keystorePropertiesFile.exists()) {
    keystorePropertiesFile.inputStream().use { stream -> keystoreProperties.load(stream) }
}

fun signingValue(key: String, env: String): String? =
    keystoreProperties.getProperty(key) ?: System.getenv(env)

val releaseStorePath: String? = signingValue("storeFile", "LEETCODINGO_KEYSTORE")
val hasReleaseKeystore: Boolean = releaseStorePath != null && file(releaseStorePath).exists()

android {
    namespace = "pl.leetcodingo"
    compileSdk = 36

    defaultConfig {
        applicationId = "pl.leetcodingo"
        minSdk = 26
        targetSdk = 36
        // Nadpisywane z linii poleceń przy wydaniu: -PversionCode=... -PversionName=...
        // Bez tego każde wydanie miałoby ten sam versionCode, a Android nie uznałby
        // nowego APK za aktualizację poprzedniego.
        versionCode = (findProperty("versionCode") as String?)?.toInt() ?: 1
        versionName = (findProperty("versionName") as String?) ?: "0.1"
    }

    sourceSets {
        getByName("main") {
            assets.srcDir(layout.buildDirectory.dir("generated/corpus"))
        }
    }

    signingConfigs {
        if (hasReleaseKeystore) {
            create("release") {
                storeFile = file(releaseStorePath!!)
                storePassword = signingValue("storePassword", "LEETCODINGO_STORE_PASSWORD")
                keyAlias = signingValue("keyAlias", "LEETCODINGO_KEY_ALIAS")
                keyPassword = signingValue("keyPassword", "LEETCODINGO_KEY_PASSWORD")
            }
        }
    }

    buildTypes {
        release {
            isMinifyEnabled = true
            isShrinkResources = true
            proguardFiles(
                getDefaultProguardFile("proguard-android-optimize.txt"),
                "proguard-rules.pro",
            )
            signingConfig = if (hasReleaseKeystore) {
                signingConfigs.getByName("release")
            } else {
                signingConfigs.getByName("debug")
            }
        }
    }

    compileOptions {
        sourceCompatibility = JavaVersion.VERSION_17
        targetCompatibility = JavaVersion.VERSION_17
    }

    kotlin {
        compilerOptions {
            jvmTarget.set(org.jetbrains.kotlin.gradle.dsl.JvmTarget.JVM_17)
        }
    }

    buildFeatures {
        compose = true
    }
}

tasks.named("preBuild") { dependsOn(copyCorpus) }

tasks.matching { it.name == "assembleRelease" }.configureEach {
    doFirst {
        if (!hasReleaseKeystore) {
            logger.warn(
                "UWAGA: brak klucza release, APK zostanie podpisane kluczem debugowym. " +
                    "Takie APK nadaje się do sprawdzenia u siebie, ale nie do rozdawania: " +
                    "klucz debugowy jest przywiązany do maszyny, więc aktualizacja zbudowana " +
                    "gdzie indziej nie zainstaluje się na wierzch i skasuje postęp."
            )
        }
    }
}

dependencies {
    implementation(libs.androidx.core.ktx)
    implementation(libs.androidx.activity.compose)
    implementation(libs.androidx.lifecycle.runtime.ktx)
    implementation(libs.androidx.lifecycle.viewmodel.compose)
    implementation(libs.androidx.lifecycle.runtime.compose)
    implementation(platform(libs.androidx.compose.bom))
    implementation(libs.androidx.compose.ui)
    implementation(libs.androidx.compose.ui.graphics)
    implementation(libs.androidx.compose.ui.tooling.preview)
    implementation(libs.androidx.compose.material3)
    implementation(libs.androidx.datastore.preferences)
    implementation(libs.kotlinx.serialization.json)
    debugImplementation(libs.androidx.compose.ui.tooling)
    testImplementation(libs.junit)
}
