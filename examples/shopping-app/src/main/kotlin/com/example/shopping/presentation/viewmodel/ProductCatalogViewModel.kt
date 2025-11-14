package com.example.shopping.presentation.viewmodel

import androidx.lifecycle.ViewModel
import androidx.lifecycle.viewModelScope
import com.example.shopping.domain.usecase.GetProductCatalogUseCase
import com.example.shopping.presentation.state.ProductCatalogAction
import com.example.shopping.presentation.state.ProductCatalogEvent
import com.example.shopping.presentation.state.ProductCatalogState
import dagger.hilt.android.lifecycle.HiltViewModel
import kotlinx.coroutines.channels.Channel
import kotlinx.coroutines.flow.*
import kotlinx.coroutines.launch
import javax.inject.Inject

// SPEC-002: ViewModel
@HiltViewModel
class ProductCatalogViewModel @Inject constructor(
    private val getProductCatalogUseCase: GetProductCatalogUseCase,
) : ViewModel() {

    private val _state = MutableStateFlow(ProductCatalogState())
    val state: StateFlow<ProductCatalogState> = _state.asStateFlow()

    private val _events = Channel<ProductCatalogEvent>()
    val events = _events.receiveAsFlow()

    fun onAction(action: ProductCatalogAction) {
        when (action) {
            is ProductCatalogAction.Load -> load(action.id)
        }
    }

    private fun load(id: String) {
        viewModelScope.launch {
            _state.update { it.copy(isLoading = true, error = null) }

            getProductCatalogUseCase(id)
                .onSuccess { data ->
                    _state.update { it.copy(isLoading = false, data = data) }
                }
                .onFailure { error ->
                    _state.update { it.copy(isLoading = false, error = error.message) }
                    _events.send(ProductCatalogEvent.ShowError(error.message ?: "Unknown error"))
                }
        }
    }
}
