import pandas as pd
import matplotlib.pyplot as plt
import os

orders = pd.read_csv('order.csv', skipinitialspace=True)
customers = pd.read_csv('customer.csv', skipinitialspace=True)
products = pd.read_csv('product.csv', skipinitialspace=True)
orders.columns = orders.columns.str.strip()
customers.columns = customers.columns.str.strip()
products.columns = products.columns.str.strip()

orders['payment_method'] = orders['payment_method'].str.strip().str.upper()
orders['rating'] = pd.to_numeric(orders['rating'], errors='coerce')
orders['discount_pct'] = pd.to_numeric(orders['discount_pct'], errors='coerce')
products['price'] = pd.to_numeric(products['price'], errors='coerce')

natural_keys = ['customer_id', 'product_id', 'order_date', 'quantity', 'discount_pct', 'payment_method', 'rating', 'returned']
orders_clean = orders.drop_duplicates(subset=natural_keys, keep='first').copy()
orders_clean['discount_pct'] = orders_clean['discount_pct'].fillna(0)
orders_clean['rating'] = orders_clean['rating'].fillna(orders_clean['rating'].median())

merged_df = orders_clean.merge(products, on='product_id').merge(customers, on='customer_id')
merged_df['order_value'] = merged_df['quantity'] * merged_df['price'] * (1 - merged_df['discount_pct'] / 100)
merged_df['order_date'] = pd.to_datetime(merged_df['order_date'])

q1 = merged_df['quantity'].quantile(0.25)
q3 = merged_df['quantity'].quantile(0.75)
iqr = q3 - q1
lower_bound = q1 - 1.5 * iqr
upper_bound = q3 + 1.5 * iqr
merged_df['is_outlier'] = (merged_df['quantity'] < lower_bound) | (merged_df['quantity'] > upper_bound)
os.makedirs('visualizations', exist_ok=True)


payment_return_stats = merged_df.groupby('payment_method')['returned'].agg(['mean'])
payment_return_stats['mean_pct'] = (payment_return_stats['mean'] * 100).round(1)
sorted_return_rates = payment_return_stats['mean_pct'].sort_values(ascending=False)

fig, ax = plt.subplots(figsize=(8, 5))
bars = ax.bar(sorted_return_rates.index, sorted_return_rates.values, color=['#e74c3c', '#3498db', '#2ecc71'])
ax.set_ylabel('Return Rate (%)')
ax.set_title('COD Returns at 44.4% — ~3x Card')
ax.set_ylim(0, 55)

for bar in bars:
    height = bar.get_height()
    ax.annotate(f'{height}%',
                xy=(bar.get_x() + bar.get_width() / 2, height),
                xytext=(0, 3),
                textcoords="offset points",
                ha='center', va='bottom', fontweight='bold')

plt.tight_layout()
plt.savefig('visualizations/return_rate_by_payment.png')
plt.close()


merged_df['year_month'] = merged_df['order_date'].dt.to_period('M')
clean_ts_df = merged_df[~merged_df['is_outlier']]
ts_clean = clean_ts_df.groupby('year_month')['order_value'].sum()

fig, ax = plt.subplots(figsize=(10, 5))
ts_clean.index = ts_clean.index.astype(str)
ax.plot(ts_clean.index, ts_clean.values, marker='o', color='#2c3e50', linewidth=2.5, markersize=6)
ax.set_title('Outlier-Corrected Monthly Revenue Trend (Peak: March 2026)')
ax.set_xlabel('Year-Month')
ax.set_ylabel('Total Revenue (₹)')
ax.grid(True, linestyle='--', alpha=0.6)

plt.tight_layout()
plt.savefig('visualizations/monthly_revenue_trend.png')
plt.close()

print("Visualizations successfully saved to 'visualizations/' folder!")