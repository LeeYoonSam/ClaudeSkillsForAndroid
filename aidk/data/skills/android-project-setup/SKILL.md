---
name: android-project-setup
description: Initialize new Android project with modern build configuration using Gradle Kotlin DSL, version catalogs, and recommended project structure. Use when starting a new Android app or module.
---

# Android Project Setup

Initialize a modern Android project with best practices for 2025.

## When to Use
- Starting a new Android application
- Adding a new module to existing project
- Modernizing legacy project structure
- Setting up build configuration

## Project Structure

### Standard Android Project Layout
```
app/
├── src/
│   ├── main/
│   │   ├── java/com/company/app/
│   │   │   ├── di/              # Dependency injection modules
│   │   │   ├── data/            # Data layer
│   │   │   │   ├── local/       # Room database, DataStore
│   │   │   │   ├── remote/      # Retrofit API services
│   │   │   │   └── repository/  # Repository implementations
│   │   │   ├── domain/          # Domain layer (optional)
│   │   │   │   ├── model/       # Domain models
│   │   │   │   └── usecase/     # Use cases
│   │   │   └── presentation/    # Presentation layer
│   │   │       ├── ui/          # Compose UI or Activities/Fragments
│   │   │       └── viewmodel/   # ViewModels
│   │   ├── res/                 # Resources
│   │   └── AndroidManifest.xml
│   ├── test/                    # Unit tests
│   └── androidTest/             # Instrumentation tests
└── build.gradle.kts
```

## Build Configuration

### Root `build.gradle.kts`
```kotlin
plugins {
    alias(libs.plugins.android.application) apply false
    alias(libs.plugins.kotlin.android) apply false
    alias(libs.plugins.kotlin.compose) apply false
    alias(libs.plugins.hilt) apply false
    alias(libs.plugins.ksp) apply false
}
```

### App Module `build.gradle.kts`
```kotlin
plugins {
    alias(libs.plugins.android.application)
    alias(libs.plugins.kotlin.android)
    alias(libs.plugins.kotlin.compose)
    alias(libs.plugins.hilt)
    alias(libs.plugins.ksp)
}

android {
    namespace = "com.company.app"
    compileSdk = 35

    defaultConfig {
        applicationId = "com.company.app"
        minSdk = 24
        targetSdk = 35
        versionCode = 1
        versionName = "1.0.0"

        testInstrumentationRunner = "androidx.test.runner.AndroidJUnitRunner"
    }

    buildTypes {
        release {
            isMinifyEnabled = true
            isShrinkResources = true
            proguardFiles(
                getDefaultProguardFile("proguard-android-optimize.txt"),
                "proguard-rules.pro"
            )
        }
        debug {
            isMinifyEnabled = false
            applicationIdSuffix = ".debug"
            versionNameSuffix = "-debug"
        }
    }

    compileOptions {
        sourceCompatibility = JavaVersion.VERSION_17
        targetCompatibility = JavaVersion.VERSION_17
    }

    kotlinOptions {
        jvmTarget = "17"
    }

    buildFeatures {
        compose = true
        buildConfig = true
    }
}

dependencies {
    // Core Android
    implementation(libs.androidx.core.ktx)
    implementation(libs.androidx.lifecycle.runtime.ktx)
    implementation(libs.androidx.activity.compose)

    // Compose BOM
    implementation(platform(libs.androidx.compose.bom))
    implementation(libs.androidx.compose.ui)
    implementation(libs.androidx.compose.ui.graphics)
    implementation(libs.androidx.compose.ui.tooling.preview)
    implementation(libs.androidx.compose.material3)

    // Hilt
    implementation(libs.hilt.android)
    ksp(libs.hilt.compiler)

    // Testing
    testImplementation(libs.junit)
    androidTestImplementation(libs.androidx.junit)
    androidTestImplementation(libs.androidx.espresso.core)
    androidTestImplementation(platform(libs.androidx.compose.bom))
    androidTestImplementation(libs.androidx.compose.ui.test.junit4)
    debugImplementation(libs.androidx.compose.ui.tooling)
    debugImplementation(libs.androidx.compose.ui.test.manifest)
}
```

### Version Catalog `gradle/libs.versions.toml`
```toml
[versions]
agp = "8.7.3"
kotlin = "2.1.0"
compose-bom = "2025.01.00"
hilt = "2.51"
ksp = "2.1.0-1.0.29"
core-ktx = "1.15.0"
lifecycle = "2.8.7"
activity-compose = "1.9.3"
navigation = "2.8.5"
room = "2.6.1"
retrofit = "2.11.0"
okhttp = "4.12.0"
coil = "3.0.4"

[libraries]
androidx-core-ktx = { group = "androidx.core", name = "core-ktx", version.ref = "core-ktx" }
androidx-lifecycle-runtime-ktx = { group = "androidx.lifecycle", name = "lifecycle-runtime-ktx", version.ref = "lifecycle" }
androidx-activity-compose = { group = "androidx.activity", name = "activity-compose", version.ref = "activity-compose" }

# Compose BOM
androidx-compose-bom = { group = "androidx.compose", name = "compose-bom", version.ref = "compose-bom" }
androidx-compose-ui = { group = "androidx.compose.ui", name = "ui" }
androidx-compose-ui-graphics = { group = "androidx.compose.ui", name = "ui-graphics" }
androidx-compose-ui-tooling = { group = "androidx.compose.ui", name = "ui-tooling" }
androidx-compose-ui-tooling-preview = { group = "androidx.compose.ui", name = "ui-tooling-preview" }
androidx-compose-ui-test-manifest = { group = "androidx.compose.ui", name = "ui-test-manifest" }
androidx-compose-ui-test-junit4 = { group = "androidx.compose.ui", name = "ui-test-junit4" }
androidx-compose-material3 = { group = "androidx.compose.material3", name = "material3" }

# Hilt
hilt-android = { group = "com.google.dagger", name = "hilt-android", version.ref = "hilt" }
hilt-compiler = { group = "com.google.dagger", name = "hilt-compiler", version.ref = "hilt" }

# Testing
junit = { group = "junit", name = "junit", version = "4.13.2" }
androidx-junit = { group = "androidx.test.ext", name = "junit", version = "1.2.1" }
androidx-espresso-core = { group = "androidx.test.espresso", name = "espresso-core", version = "3.6.1" }

[plugins]
android-application = { id = "com.android.application", version.ref = "agp" }
kotlin-android = { id = "org.jetbrains.kotlin.android", version.ref = "kotlin" }
kotlin-compose = { id = "org.jetbrains.kotlin.plugin.compose", version.ref = "kotlin" }
hilt = { id = "com.google.dagger.hilt.android", version.ref = "hilt" }
ksp = { id = "com.google.devtools.ksp", version.ref = "ksp" }
```

### `gradle.properties`
```properties
# Kotlin
kotlin.code.style=official

# Android
android.useAndroidX=true
android.nonTransitiveRClass=true

# Build Performance
org.gradle.jvmargs=-Xmx2048m -Dfile.encoding=UTF-8
org.gradle.parallel=true
org.gradle.caching=true
org.gradle.configuration-cache=true

# R8
android.enableR8.fullMode=true
```

## AndroidManifest.xml

```xml
<?xml version="1.0" encoding="utf-8"?>
<manifest xmlns:android="http://schemas.android.com/apk/res/android">

    <uses-permission android:name="android.permission.INTERNET" />

    <application
        android:name=".MyApplication"
        android:allowBackup="true"
        android:icon="@mipmap/ic_launcher"
        android:label="@string/app_name"
        android:roundIcon="@mipmap/ic_launcher_round"
        android:supportsRtl="true"
        android:theme="@style/Theme.App">
        <activity
            android:name=".MainActivity"
            android:exported="true"
            android:theme="@style/Theme.App">
            <intent-filter>
                <action android:name="android.intent.action.MAIN" />
                <category android:name="android.intent.category.LAUNCHER" />
            </intent-filter>
        </activity>
    </application>

</manifest>
```

## Application Class

```kotlin
package com.company.app

import android.app.Application
import dagger.hilt.android.HiltAndroidApp

@HiltAndroidApp
class MyApplication : Application() {
    override fun onCreate() {
        super.onCreate()
        // Initialize app-level components
    }
}
```

## MainActivity (Compose)

```kotlin
package com.company.app

import android.os.Bundle
import androidx.activity.ComponentActivity
import androidx.activity.compose.setContent
import androidx.activity.enableEdgeToEdge
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.padding
import androidx.compose.material3.Scaffold
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.ui.Modifier
import androidx.compose.ui.tooling.preview.Preview
import com.company.app.presentation.theme.AppTheme
import dagger.hilt.android.AndroidEntryPoint

@AndroidEntryPoint
class MainActivity : ComponentActivity() {
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        enableEdgeToEdge()
        setContent {
            AppTheme {
                Scaffold(modifier = Modifier.fillMaxSize()) { innerPadding ->
                    Greeting(
                        name = "Android",
                        modifier = Modifier.padding(innerPadding)
                    )
                }
            }
        }
    }
}

@Composable
fun Greeting(name: String, modifier: Modifier = Modifier) {
    Text(
        text = "Hello $name!",
        modifier = modifier
    )
}

@Preview(showBackground = true)
@Composable
fun GreetingPreview() {
    AppTheme {
        Greeting("Android")
    }
}
```

## ProGuard Rules

Create `app/proguard-rules.pro`:
```proguard
# Keep BuildConfig
-keep class **.BuildConfig { *; }

# Retrofit
-keepattributes Signature, InnerClasses, EnclosingMethod
-keepattributes RuntimeVisibleAnnotations, RuntimeVisibleParameterAnnotations
-keepclassmembers,allowshrinking,allowobfuscation interface * {
    @retrofit2.http.* <methods>;
}

# OkHttp
-dontwarn okhttp3.**
-dontwarn okio.**

# Gson
-keepattributes Signature
-keepattributes *Annotation*
-keep class com.google.gson.** { *; }

# Coroutines
-keepnames class kotlinx.coroutines.internal.MainDispatcherFactory {}
-keepnames class kotlinx.coroutines.CoroutineExceptionHandler {}
```

## Related Skills
- For dependency injection setup, see: **android-hilt-di** or **android-koin-di**
- For UI implementation, see: **android-compose-ui** or **android-xml-views**
- For architecture patterns, see: **android-mvvm-architecture** and **android-clean-architecture**
- For navigation, see: **android-compose-navigation**

## Best Practices
1. **Use Version Catalogs**: Centralize dependency versions in `libs.versions.toml`
2. **Enable R8**: Configure full mode for optimal code shrinking
3. **Kotlin DSL**: Prefer `.gradle.kts` over `.gradle` for type safety
4. **Namespace**: Always set explicit namespace in build.gradle.kts
5. **Build Performance**: Enable parallel execution, caching, and configuration cache
6. **Minimum SDK**: Target API 24+ (covers 98%+ of devices in 2025)
7. **Java 17**: Use Java 17 for Kotlin compilation target
8. **Edge-to-Edge**: Enable edge-to-edge display in modern apps
