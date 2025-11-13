---
name: android-forms-validation
description: Create forms with validation in Jetpack Compose using state and validation logic. Use when building input forms with real-time validation.
---

# Forms and Validation

Build forms with validation in Jetpack Compose.

## Form State

```kotlin
data class LoginFormState(
    val email: String = "",
    val emailError: String? = null,
    val password: String = "",
    val passwordError: String? = null,
    val isFormValid: Boolean = false
)

@HiltViewModel
class LoginViewModel @Inject constructor() : ViewModel() {

    private val _formState = MutableStateFlow(LoginFormState())
    val formState: StateFlow<LoginFormState> = _formState.asStateFlow()

    fun onEmailChange(email: String) {
        _formState.update {
            it.copy(
                email = email,
                emailError = validateEmail(email)
            )
        }
        updateFormValidity()
    }

    fun onPasswordChange(password: String) {
        _formState.update {
            it.copy(
                password = password,
                passwordError = validatePassword(password)
            )
        }
        updateFormValidity()
    }

    private fun validateEmail(email: String): String? {
        return when {
            email.isBlank() -> "Email is required"
            !android.util.Patterns.EMAIL_ADDRESS.matcher(email).matches() ->
                "Invalid email format"
            else -> null
        }
    }

    private fun validatePassword(password: String): String? {
        return when {
            password.isBlank() -> "Password is required"
            password.length < 8 -> "Password must be at least 8 characters"
            else -> null
        }
    }

    private fun updateFormValidity() {
        _formState.update {
            it.copy(
                isFormValid = it.emailError == null &&
                        it.passwordError == null &&
                        it.email.isNotBlank() &&
                        it.password.isNotBlank()
            )
        }
    }

    fun submit() {
        if (formState.value.isFormValid) {
            // Submit form
        }
    }
}
```

## Form UI

```kotlin
@Composable
fun LoginForm(viewModel: LoginViewModel = hiltViewModel()) {
    val formState by viewModel.formState.collectAsStateWithLifecycle()

    Column(
        modifier = Modifier
            .fillMaxSize()
            .padding(16.dp),
        verticalArrangement = Arrangement.spacedBy(16.dp)
    ) {
        OutlinedTextField(
            value = formState.email,
            onValueChange = viewModel::onEmailChange,
            label = { Text("Email") },
            isError = formState.emailError != null,
            supportingText = formState.emailError?.let { { Text(it) } },
            keyboardOptions = KeyboardOptions(keyboardType = KeyboardType.Email),
            modifier = Modifier.fillMaxWidth()
        )

        OutlinedTextField(
            value = formState.password,
            onValueChange = viewModel::onPasswordChange,
            label = { Text("Password") },
            isError = formState.passwordError != null,
            supportingText = formState.passwordError?.let { { Text(it) } },
            visualTransformation = PasswordVisualTransformation(),
            keyboardOptions = KeyboardOptions(keyboardType = KeyboardType.Password),
            modifier = Modifier.fillMaxWidth()
        )

        Button(
            onClick = viewModel::submit,
            enabled = formState.isFormValid,
            modifier = Modifier.fillMaxWidth()
        ) {
            Text("Login")
        }
    }
}
```

## Best Practices
1. Validate on text change for real-time feedback
2. Show errors only after user interaction
3. Disable submit button when form invalid
4. Use appropriate keyboard types
5. Provide clear error messages
