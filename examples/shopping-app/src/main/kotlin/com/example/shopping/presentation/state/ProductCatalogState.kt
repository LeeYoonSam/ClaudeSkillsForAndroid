package com.example.shopping.presentation.state

import com.example.shopping.domain.model.ProductCatalog

// SPEC-002: Screen state
data class ProductCatalogState(
    val isLoading: Boolean = false,
    val data: ProductCatalog? = null,
    val error: String? = null,
)

// SPEC-002: User actions
sealed interface ProductCatalogAction {
    data class Load(val id: String) : ProductCatalogAction
}

// SPEC-002: One-time events
sealed interface ProductCatalogEvent {
    data class ShowError(val message: String) : ProductCatalogEvent
}
