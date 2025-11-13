---
name: android-permissions
description: Handle runtime permissions for Android 13+ with permission requests and rationale. Use when implementing features requiring dangerous permissions.
---

# Runtime Permissions

Handle Android runtime permissions properly.

## Manifest

```xml
<uses-permission android:name="android.permission.CAMERA" />
<uses-permission android:name="android.permission.READ_MEDIA_IMAGES" />
<uses-permission android:name="android.permission.ACCESS_FINE_LOCATION" />
```

## Compose (with Accompanist)

```kotlin
@Composable
fun CameraScreen() {
    val cameraPermissionState = rememberPermissionState(
        android.Manifest.permission.CAMERA
    )

    when {
        cameraPermissionState.status.isGranted -> {
            CameraView()
        }
        cameraPermissionState.status.shouldShowRationale -> {
            PermissionRationale(
                onRequestPermission = { cameraPermissionState.launchPermissionRequest() }
            )
        }
        else -> {
            Button(onClick = { cameraPermissionState.launchPermissionRequest() }) {
                Text("Grant Camera Permission")
            }
        }
    }
}

// Multiple permissions
@Composable
fun LocationScreen() {
    val permissionsState = rememberMultiplePermissionsState(
        permissions = listOf(
            android.Manifest.permission.ACCESS_FINE_LOCATION,
            android.Manifest.permission.ACCESS_COARSE_LOCATION
        )
    )

    if (permissionsState.allPermissionsGranted) {
        MapView()
    } else {
        Button(onClick = { permissionsState.launchMultiplePermissionRequest() }) {
            Text("Grant Location Permissions")
        }
    }
}
```

## Activity/Fragment

```kotlin
class CameraFragment : Fragment() {

    private val requestPermissionLauncher = registerForActivityResult(
        ActivityResultContracts.RequestPermission()
    ) { isGranted ->
        if (isGranted) {
            openCamera()
        } else {
            showPermissionDeniedMessage()
        }
    }

    private fun checkAndRequestPermission() {
        when {
            ContextCompat.checkSelfPermission(
                requireContext(),
                Manifest.permission.CAMERA
            ) == PackageManager.PERMISSION_GRANTED -> {
                openCamera()
            }
            shouldShowRequestPermissionRationale(Manifest.permission.CAMERA) -> {
                showRationale()
            }
            else -> {
                requestPermissionLauncher.launch(Manifest.permission.CAMERA)
            }
        }
    }
}
```

## Best Practices
1. Request permissions when needed, not upfront
2. Explain why permission is needed
3. Handle denied permissions gracefully
4. Use Accompanist for Compose
5. Check permissions before using features
