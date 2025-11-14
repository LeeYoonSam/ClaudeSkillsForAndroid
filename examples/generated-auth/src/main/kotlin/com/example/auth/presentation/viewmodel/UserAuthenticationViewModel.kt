package com.example.auth.presentation.viewmodel

import androidx.lifecycle.ViewModel
import androidx.lifecycle.viewModelScope
import com.example.auth.domain.usecase.GetUserAuthenticationUseCase
import com.example.auth.presentation.state.UserAuthenticationAction
import com.example.auth.presentation.state.UserAuthenticationEvent
import com.example.auth.presentation.state.UserAuthenticationState
import dagger.hilt.android.lifecycle.HiltViewModel
import kotlinx.coroutines.channels.Channel
import kotlinx.coroutines.flow.*
import kotlinx.coroutines.launch
import javax.inject.Inject

// SPEC-001: ViewModel
@HiltViewModel
class UserAuthenticationViewModel @Inject constructor(
    private val getUserAuthenticationUseCase: GetUserAuthenticationUseCase,
) : ViewModel() {

    private val _state = MutableStateFlow(UserAuthenticationState())
    val state: StateFlow<UserAuthenticationState> = _state.asStateFlow()

    private val _events = Channel<UserAuthenticationEvent>()
    val events = _events.receiveAsFlow()

    fun onAction(action: UserAuthenticationAction) {
        when (action) {
            is UserAuthenticationAction.Load -> load(action.id)
        }
    }

    private fun load(id: String) {
        viewModelScope.launch {
            _state.update { it.copy(isLoading = true, error = null) }

            getUserAuthenticationUseCase(id)
                .onSuccess { data ->
                    _state.update { it.copy(isLoading = false, data = data) }
                }
                .onFailure { error ->
                    _state.update { it.copy(isLoading = false, error = error.message) }
                    _events.send(UserAuthenticationEvent.ShowError(error.message ?: "Unknown error"))
                }
        }
    }
}
