find originals/ -type f -name "*.webp" -exec basename {} .webp ';' | xargs -I{} magick {}.webp -resize 25% -quality 85 {}.jpg
