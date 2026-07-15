#include <metal_stdlib>
using namespace metal;

[[ stitchable ]] half4 waveColor(float2 position, half4 color, float time) {
    float angle = position.x * 0.05 + time * 3.0;
    half factor = half(sin(angle) * 0.5 + 0.5);
    return mix(color, half4(0.2, 0.6, 1.0, 1.0), factor * 0.4);
}
