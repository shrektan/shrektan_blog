# 配图生成记录

## img-01.jpg

- 生成日期：2026-08-05
- 模型：`bytedance/seedream-4`（Replicate）
- 参数：`aspect_ratio: 16:9`，`image_size: 1024x576`
- 后处理：PIL 白边裁剪（bbox 52,112,2560,1440）
- 位置：「世界变了，它还没来得及变」那句之后；同时作为 OG 封面。（初稿放在第一节收尾处，审稿指出那里紧跟「黑漆漆的小路」那个例子，读者会误以为图在画那条小路——而画面是明亮的黄昏城市，对不上。移到 thesis 那句下面就对上了。）
- 已知瑕疵：prompt 要的是「影子本身隐约带四足动物轮廓」，实际渲染成了人影 + 一只独立的狗，视觉双关没完全合上。移位后语境足够，未重新生成。
- 构思 thesis：直觉是几十亿年进化攒下来的经验，它救过我们的命，但它是在旧世界里攒的——世界变了，它没跟上。画面扣的是「带着旧世界的东西走在新世界里」，不是文中「黑夜小路」那个论据。

Prompt：

```
Minimalist watercolor illustration on pure white background, soft muted colors,
gentle brush strokes, lots of negative space, hand-drawn feel, editorial blog
aesthetic, no text. A lone modern person in a plain coat walking along an empty
city sidewalk in late afternoon light, seen from behind at a distance, small in
the frame. Their long cast shadow stretches far across the pavement, but the
shadow is not quite human — its silhouette subtly carries the low crouching
outline of a four-legged animal. Pale grey and warm ochre tones with one soft
muted blue accent. Vast empty white space around the figure, sparse composition,
quiet and contemplative mood.
```
