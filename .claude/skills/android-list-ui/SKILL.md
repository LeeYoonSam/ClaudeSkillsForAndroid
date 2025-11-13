---
name: android-list-ui
description: Build efficient lists with LazyColumn (Compose) or RecyclerView (Views) including item click handling. Use when displaying scrollable lists of data.
---

# List UI

Build efficient scrollable lists with LazyColumn or RecyclerView.

## LazyColumn (Compose)

```kotlin
@Composable
fun ProductList(
    products: List<Product>,
    onProductClick: (Product) -> Unit,
    modifier: Modifier = Modifier
) {
    LazyColumn(
        modifier = modifier.fillMaxSize(),
        contentPadding = PaddingValues(16.dp),
        verticalArrangement = Arrangement.spacedBy(8.dp)
    ) {
        items(
            items = products,
            key = { it.id }
        ) { product ->
            ProductItem(
                product = product,
                onClick = { onProductClick(product) }
            )
        }
    }
}

@Composable
fun ProductItem(
    product: Product,
    onClick: () -> Unit,
    modifier: Modifier = Modifier
) {
    Card(
        modifier = modifier
            .fillMaxWidth()
            .clickable { onClick() },
        elevation = CardDefaults.cardElevation(2.dp)
    ) {
        Row(
            modifier = Modifier.padding(16.dp),
            verticalAlignment = Alignment.CenterVertically
        ) {
            AsyncImage(
                model = product.imageUrl,
                contentDescription = null,
                modifier = Modifier.size(64.dp)
            )
            Spacer(modifier = Modifier.width(16.dp))
            Column {
                Text(
                    text = product.name,
                    style = MaterialTheme.typography.titleMedium
                )
                Text(
                    text = "$${product.price}",
                    style = MaterialTheme.typography.bodyMedium
                )
            }
        }
    }
}
```

## LazyVerticalGrid

```kotlin
@Composable
fun ProductGrid(
    products: List<Product>,
    onProductClick: (Product) -> Unit
) {
    LazyVerticalGrid(
        columns = GridCells.Fixed(2),
        contentPadding = PaddingValues(16.dp),
        horizontalArrangement = Arrangement.spacedBy(8.dp),
        verticalArrangement = Arrangement.spacedBy(8.dp)
    ) {
        items(products, key = { it.id }) { product ->
            ProductCard(product, onClick = { onProductClick(product) })
        }
    }
}
```

## RecyclerView (Views)

```kotlin
class ProductAdapter(
    private val onItemClick: (Product) -> Unit
) : ListAdapter<Product, ProductAdapter.ViewHolder>(DiffCallback()) {

    override fun onCreateViewHolder(parent: ViewGroup, viewType: Int): ViewHolder {
        val binding = ItemProductBinding.inflate(
            LayoutInflater.from(parent.context),
            parent,
            false
        )
        return ViewHolder(binding, onItemClick)
    }

    override fun onBindViewHolder(holder: ViewHolder, position: Int) {
        holder.bind(getItem(position))
    }

    class ViewHolder(
        private val binding: ItemProductBinding,
        private val onItemClick: (Product) -> Unit
    ) : RecyclerView.ViewHolder(binding.root) {

        fun bind(product: Product) {
            binding.nameText.text = product.name
            binding.priceText.text = "$${product.price}"
            Glide.with(binding.root.context)
                .load(product.imageUrl)
                .into(binding.imageView)

            binding.root.setOnClickListener {
                onItemClick(product)
            }
        }
    }

    class DiffCallback : DiffUtil.ItemCallback<Product>() {
        override fun areItemsTheSame(oldItem: Product, newItem: Product) =
            oldItem.id == newItem.id

        override fun areContentsTheSame(oldItem: Product, newItem: Product) =
            oldItem == newItem
    }
}

// Usage
binding.recyclerView.apply {
    layoutManager = LinearLayoutManager(context)
    adapter = ProductAdapter { product ->
        // Handle click
    }
}

productAdapter.submitList(products)
```

## Best Practices
1. Always provide `key` parameter in Compose items
2. Use `LazyColumn` instead of `Column` with scroll
3. Use `ListAdapter` with `DiffUtil` for RecyclerView
4. Avoid nested scrolling when possible
5. Use appropriate spacing and padding
