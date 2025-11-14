package com.example.shopping.presentation.ui

import androidx.compose.foundation.layout.*
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.unit.dp
import androidx.hilt.navigation.compose.hiltViewModel
import androidx.lifecycle.compose.collectAsStateWithLifecycle
import com.example.shopping.presentation.state.ProductCatalogAction
import com.example.shopping.presentation.state.ProductCatalogEvent
import com.example.shopping.presentation.viewmodel.ProductCatalogViewModel

// SPEC-002: Screen
@Composable
fun ProductCatalogScreen(
    viewModel: ProductCatalogViewModel = hiltViewModel(),
) {
    val state by viewModel.state.collectAsStateWithLifecycle()

    LaunchedEffect(Unit) {
        viewModel.events.collect { event ->
            when (event) {
                is ProductCatalogEvent.ShowError -> {
                    // TODO: Show snackbar or toast
                }
            }
        }
    }

    ProductCatalogContent(
        state = state,
        onAction = viewModel::onAction,
    )
}

@Composable
private fun ProductCatalogContent(
    state: ProductCatalogState,
    onAction: (ProductCatalogAction) -> Unit,
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
