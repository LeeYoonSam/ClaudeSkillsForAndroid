---
name: android-gradle-config
description: Configure Gradle build with Kotlin DSL including build types, flavors, and dependencies. Use when setting up project build configuration.
---

# Gradle Configuration

Configure Android build with Gradle Kotlin DSL.

## Build Types

```kotlin
android {
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
}
```

## Product Flavors

```kotlin
android {
    flavorDimensions += "environment"

    productFlavors {
        create("dev") {
            dimension = "environment"
            applicationIdSuffix = ".dev"
            versionNameSuffix = "-dev"
            buildConfigField("String", "API_URL", "\"https://dev-api.example.com\"")
        }

        create("staging") {
            dimension = "environment"
            applicationIdSuffix = ".staging"
            buildConfigField("String", "API_URL", "\"https://staging-api.example.com\"")
        }

        create("prod") {
            dimension = "environment"
            buildConfigField("String", "API_URL", "\"https://api.example.com\"")
        }
    }
}
```

## Version Catalogs

```toml
# gradle/libs.versions.toml
[versions]
agp = "8.7.3"
kotlin = "2.1.0"
compose-bom = "2025.01.00"

[libraries]
androidx-core-ktx = { group = "androidx.core", name = "core-ktx", version = "1.15.0" }
androidx-compose-bom = { group = "androidx.compose", name = "compose-bom", version.ref = "compose-bom" }

[plugins]
android-application = { id = "com.android.application", version.ref = "agp" }
kotlin-android = { id = "org.jetbrains.kotlin.android", version.ref = "kotlin" }
```

## Dependencies

```kotlin
dependencies {
    // Using version catalog
    implementation(libs.androidx.core.ktx)
    implementation(platform(libs.androidx.compose.bom))

    // Implementation vs API
    implementation(libs.retrofit) // Not exposed to consumers
    api(libs.gson) // Exposed to consumers
}
```

## Best Practices
1. Use Kotlin DSL for type safety
2. Centralize versions in version catalog
3. Enable R8 for production
4. Use build flavors for different environments
5. Configure ProGuard rules properly
