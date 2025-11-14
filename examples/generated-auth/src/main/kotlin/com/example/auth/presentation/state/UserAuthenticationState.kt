package com.example.auth.presentation.state

import com.example.auth.domain.model.UserAuthentication

// SPEC-001: Screen state
data class UserAuthenticationState(
    val isLoading: Boolean = false,
    val data: UserAuthentication? = null,
    val error: String? = null,
)

// SPEC-001: User actions
sealed interface UserAuthenticationAction {
    data class Load(val id: String) : UserAuthenticationAction
}

// SPEC-001: One-time events
sealed interface UserAuthenticationEvent {
    data class ShowError(val message: String) : UserAuthenticationEvent
}
