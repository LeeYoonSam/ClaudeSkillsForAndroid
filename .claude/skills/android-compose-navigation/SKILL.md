---
name: android-compose-navigation
description: Implement Navigation 3 for Jetpack Compose with type-safe routes, nested navigation, and deep linking. Use when handling screen navigation in Compose apps.
---

# Jetpack Compose Navigation

Implement navigation in Jetpack Compose using Navigation Component with type-safe routes.

## When to Use
- Navigating between screens in Compose apps
- Implementing bottom navigation or drawer
- Handling deep links
- Passing data between screens

## Dependencies

```kotlin
// In libs.versions.toml
[versions]
navigation = "2.8.5"

[libraries]
androidx-navigation-compose = { group = "androidx.navigation", name = "navigation-compose", version.ref = "navigation" }
androidx-hilt-navigation-compose = { group = "androidx.hilt", name = "hilt-navigation-compose", version = "1.2.0" }

// In build.gradle.kts
implementation(libs.androidx.navigation.compose)
implementation(libs.androidx.hilt.navigation.compose)
```

## Basic Navigation Setup

### Define Routes (Sealed Class)

```kotlin
sealed class Screen(val route: String) {
    data object Home : Screen("home")
    data object Profile : Screen("profile")
    data class Detail(val id: String = "{id}") : Screen("detail/$id") {
        fun createRoute(id: String) = "detail/$id"
    }
}
```

### NavHost Setup

```kotlin
@Composable
fun AppNavigation(
    navController: NavHostController = rememberNavController()
) {
    NavHost(
        navController = navController,
        startDestination = Screen.Home.route
    ) {
        composable(Screen.Home.route) {
            HomeScreen(
                onNavigateToDetail = { id ->
                    navController.navigate(Screen.Detail().createRoute(id))
                }
            )
        }

        composable(
            route = Screen.Detail().route,
            arguments = listOf(
                navArgument("id") { type = NavType.StringType }
            )
        ) { backStackEntry ->
            val id = backStackEntry.arguments?.getString("id") ?: return@composable
            DetailScreen(
                id = id,
                onNavigateBack = { navController.popBackStack() }
            )
        }
    }
}
```

## Bottom Navigation

```kotlin
sealed class BottomNavScreen(val route: String, val title: String, val icon: ImageVector) {
    data object Home : BottomNavScreen("home", "Home", Icons.Default.Home)
    data object Search : BottomNavScreen("search", "Search", Icons.Default.Search)
    data object Profile : BottomNavScreen("profile", "Profile", Icons.Default.Person)
}

@Composable
fun MainScreen() {
    val navController = rememberNavController()

    Scaffold(
        bottomBar = {
            NavigationBar {
                val navBackStackEntry by navController.currentBackStackEntryAsState()
                val currentRoute = navBackStackEntry?.destination?.route

                listOf(
                    BottomNavScreen.Home,
                    BottomNavScreen.Search,
                    BottomNavScreen.Profile
                ).forEach { screen ->
                    NavigationBarItem(
                        icon = { Icon(screen.icon, contentDescription = screen.title) },
                        label = { Text(screen.title) },
                        selected = currentRoute == screen.route,
                        onClick = {
                            navController.navigate(screen.route) {
                                popUpTo(navController.graph.findStartDestination().id) {
                                    saveState = true
                                }
                                launchSingleTop = true
                                restoreState = true
                            }
                        }
                    )
                }
            }
        }
    ) { paddingValues ->
        NavHost(
            navController = navController,
            startDestination = BottomNavScreen.Home.route,
            modifier = Modifier.padding(paddingValues)
        ) {
            composable(BottomNavScreen.Home.route) { HomeScreen() }
            composable(BottomNavScreen.Search.route) { SearchScreen() }
            composable(BottomNavScreen.Profile.route) { ProfileScreen() }
        }
    }
}
```

## Related Skills
- **android-compose-ui**: For building screen UI
- **android-mvvm-architecture**: For screen ViewModels
- **android-one-time-events**: For navigation events

## Best Practices
1. Use sealed classes for type-safe routes
2. Handle navigation in UI layer, not ViewModel
3. Use `saveState` for bottom navigation
4. Always validate navigation arguments
5. Manage back stack properly with `popUpTo`
