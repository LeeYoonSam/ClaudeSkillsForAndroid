package com.example.auth.presentation.ui

import androidx.compose.foundation.layout.*
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.unit.dp
import androidx.hilt.navigation.compose.hiltViewModel
import androidx.lifecycle.compose.collectAsStateWithLifecycle
import com.example.auth.presentation.state.UserAuthenticationAction
import com.example.auth.presentation.state.UserAuthenticationEvent
import com.example.auth.presentation.viewmodel.UserAuthenticationViewModel

// SPEC-001: Screen
@Composable
fun UserAuthenticationScreen(
    viewModel: UserAuthenticationViewModel = hiltViewModel(),
) {
    val state by viewModel.state.collectAsStateWithLifecycle()

    LaunchedEffect(Unit) {
        viewModel.events.collect { event ->
            when (event) {
                is UserAuthenticationEvent.ShowError -> {
                    // TODO: Show snackbar or toast
                }
            }
        }
    }

    UserAuthenticationContent(
        state = state,
        onAction = viewModel::onAction,
    )
}

@Composable
private fun UserAuthenticationContent(
    state: UserAuthenticationState,
    onAction: (UserAuthenticationAction) -> Unit,
) {
    Column(
        modifier = Modifier
            .fillMaxSize()
            .padding(16.dp),
        horizontalAlignment = Alignment.CenterHorizontally,
        verticalArrangement = Arrangement.Center,
    ) {
        when {
            state.isLoading -> CircularProgressIndicator()
            state.error != null -> Text("Error: ${state.error}")
            state.data != null -> Text("Data: ${state.data}")
            else -> Text("No data")
        }
    }
}
