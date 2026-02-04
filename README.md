
# Generate Product Images ❄️ → 🖼️ 

This example demonstrates:

1. ❄️ Secure data processing inside Snowflake using `@snowpark`, triggered automatically when new data is available.
2. 🚚 Efficient data movement to a GPU cloud.
3. 🧠 High-throughput autonomous inferencing, in this case, product image generation.

### The system is divided into three flows

1. `SensorFlow` which polls for changes in data periodically. When new data is available, it triggers →
2. `RetrieveDescriptions` runs inside Snowflake. Upon completion, it triggers →
3. `ProductImageFlow` which generates product images from the supplied descriptions
  in parallel.

Currently, a state-of-the-art image generation model, `Qwen-Image` is used to generate
product images, relying on efficient parallelized autonomous inferencing on Outerbounds.


