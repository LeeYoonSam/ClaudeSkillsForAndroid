---
name: android-image-loading
description: Load and display images with Coil (Compose) or Glide including caching and transformations. Use when displaying remote or local images efficiently.
---

# Image Loading

Load images efficiently with Coil (Compose) or Glide (Views).

## Coil (Compose)

```kotlin
// Dependency
implementation("io.coil-kt.coil3:coil-compose:3.0.4")
implementation("io.coil-kt.coil3:coil-network-okhttp:3.0.4")

// Basic usage
@Composable
fun ProductImage(imageUrl: String) {
    AsyncImage(
        model = imageUrl,
        contentDescription = "Product image",
        modifier = Modifier.size(200.dp),
        contentScale = ContentScale.Crop
    )
}

// With placeholder and error
@Composable
fun UserAvatar(imageUrl: String?) {
    AsyncImage(
        model = ImageRequest.Builder(LocalContext.current)
            .data(imageUrl)
            .crossfade(true)
            .build(),
        contentDescription = "User avatar",
        placeholder = painterResource(R.drawable.placeholder),
        error = painterResource(R.drawable.error),
        modifier = Modifier
            .size(64.dp)
            .clip(CircleShape)
    )
}

// With transformations
@Composable
fun BlurredImage(imageUrl: String) {
    AsyncImage(
        model = ImageRequest.Builder(LocalContext.current)
            .data(imageUrl)
            .transformations(
                CircleCropTransformation(),
                BlurTransformation(radius = 10f)
            )
            .build(),
        contentDescription = null
    )
}
```

## Glide (Views)

```kotlin
// Dependency
implementation("com.github.bumptech.glide:glide:4.16.0")
ksp("com.github.bumptech.glide:compiler:4.16.0")

// Basic usage
Glide.with(context)
    .load(imageUrl)
    .into(imageView)

// With placeholder and error
Glide.with(context)
    .load(imageUrl)
    .placeholder(R.drawable.placeholder)
    .error(R.drawable.error)
    .into(imageView)

// With transformations
Glide.with(context)
    .load(imageUrl)
    .circleCrop()
    .into(imageView)

// Custom size
Glide.with(context)
    .load(imageUrl)
    .override(300, 200)
    .centerCrop()
    .into(imageView)
```

## Best Practices
1. Use Coil for Compose, Glide for Views
2. Always provide placeholder and error images
3. Use appropriate contentScale/scaleType
4. Enable crossfade for smooth transitions
5. Cache images automatically (both libraries do this)
