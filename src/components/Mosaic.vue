<template>
  <div style="display: flex">
    <div>
      <div id="target-container"></div>
      <div>{{ targetBlock.description }} </div>
      <div>{{ targetBlock.userId }} </div>
      <div v-if="targetBlock.created_at">{{ targetBlock.created_at.split('T')[0] }} </div>
    </div>
    <div id="mosaic-container"></div>
    <div>
      <div id="explorer-container"></div>
      <div>{{ exploreBlock.description }} </div>
      <div>{{ exploreBlock.userId }} </div>
      <div v-if="exploreBlock.created_at">{{ exploreBlock.created_at.split('T')[0] }} </div>
    </div>
  </div>
</template>

<script>

import * as d3 from 'd3';
import ImageUtil from '../libs/image-util';

const BASE_W = 230;
const BASE_H = 120;

const TARGET_W = BASE_W * 2.0;
const TARGET_H = BASE_H * 2.0;

const TILE_W = 23;
const TILE_H = 12;

const DURATION = 2000;

const imageCache = new Map();

async function loadThumbnail(blocks, startIdx, endIdx, width, height) {
  // FIXME use web-workers to speed it up, or preprocess
  const r = [];
  for (let i = startIdx; i <= endIdx; i++) {
    try {
      const d = await ImageUtil.loadImage(blocks[i].thumbnail, { width, height });
      blocks[i].imageData = d;
      r.push(blocks[i]);
    } catch (err) {
      // blocks[i].imageData = null;
    }
  }
  return r;
}

const drawRGBA = (ctx, data, w, h, x = 0, y = 0) => {
  const imageData = ctx.createImageData(w, h);
  for (let i = 0; i < data.length; i++) {
    const v = data[i];
    imageData.data[i] = v;
  }
  ctx.putImageData(imageData, x, y);
};


const findBestImage = (sourceImages, target) => {
  let r = sourceImages[0];
  let dist = 999999999;
  for (let i = 0; i < sourceImages.length; i++) {
    const d = ImageUtil.distance(target, sourceImages[i].imageData.data);
    if (d < dist) {
      dist = d;
      r = sourceImages[i];
    }
  }
  return r;
};


export default {
  props: {
    blocks: {
      type: Array
    },
    targetIndex: {
      type: Number
    }
  },
  data: () => ({
    targetBlock: {},
    exploreBlock: {}
  }),
  watch: {
    targetIndex() {
      this.refresh();
    }
  },
  mounted() {
    this.refresh();
  },
  methods: {
    async refresh() {
      const blocks = this.blocks;
      const targetIndex = this.targetIndex;

      d3.select('#mosaic-container').selectAll('*').remove();
      d3.select('#target-container').selectAll('*').remove();
      d3.select('#explore-container').selectAll('*').remove();


      const rootEl = document.getElementById('mosaic-container');

      // Load a random target
      const target = (await loadThumbnail(blocks, targetIndex, targetIndex, 230, 120))[0];
      this.targetBlock = target;
      const canvas = document.createElement('canvas');
      canvas.width = target.imageData.width;
      canvas.height = target.imageData.height;
      canvas.style['z-index'] = 5;

      canvas.getContext('2d').putImageData(target.imageData, 0, 0);
      document.getElementById('target-container').append(canvas);

      // Make the target image 2X larger to better git
      const canvas2 = document.createElement('canvas');
      canvas2.id = 'target-image';
      canvas2.width = TARGET_W;
      canvas2.height = TARGET_H;
      const ctx2 = canvas2.getContext('2d');
      ctx2.drawImage(canvas, 0, 0, TARGET_W, TARGET_H);
      const targetImageData2X = ctx2.getImageData(0, 0, TARGET_W, TARGET_H);

      // 1. Load source images
      const availableBlocks = await loadThumbnail(blocks, 140, 160, TILE_W, TILE_H);
      const sourceImages = [];
      for (let i = 0; i < availableBlocks.length; i++) {
        const b = availableBlocks[i];
        sourceImages.push(b);
      }

      // 2. Chop and run best matching tile
      // FIXME: Split into web-worker threads
      for (let i = 0; i < (TARGET_W / TILE_W); i++) {
        for (let j = 0; j < (TARGET_H / TILE_H); j++) {
          const tile = ImageUtil.crop(targetImageData2X.data,
            { width: TARGET_W, height: TARGET_H, channels: 4 },
            { x: i * TILE_W, y: j * TILE_H, width: TILE_W, height: TILE_H } // reverse W and H
          );

          const best = findBestImage(sourceImages, tile);
          const canvas = document.createElement('canvas');
          canvas.width = TILE_W;
          canvas.height = TILE_H;
          // drawRGBA(canvas.getContext('2d'), tile, TILE_W, TILE_H);
          drawRGBA(canvas.getContext('2d'), best.imageData.data, TILE_W, TILE_H);
          rootEl.append(canvas);

          d3.select(canvas)
            .style('position', 'absolute')
            .style('opacity', 1)
            .style('z-index', j * TILE_W + i)
            .style('left', (Math.random() * 2000 - 1000) + 'px')
            .style('top', (Math.random() * 2000 - 1000) + 'px')
            .on('mouseover', () => {
              this.showTile(best);
            })
            .on('click', () => {
              console.log(best);
              window.open(`http://bl.ocks.org/${best.userId}/${best.id}`, '_blank');
            })
            .transition()
            .duration(DURATION)
            .style('left', i * TILE_W + 'px')
            .style('top', j * TILE_H + 'px');
        }
      }
    },
    async showTile(tile) {
      this.exploreBlock = tile;
      let imageData = null;
      if (imageCache.has(tile.id)) {
        imageData = imageCache.get(tile.id);
      } else {
        imageData = await ImageUtil.loadImage(tile.thumbnail, { BASE_W, BASE_H });
        imageCache.set(tile.id, imageData);
      }
      const explorer = document.getElementById('explorer-container');
      explorer.innerHTML = '';
      const canvas = document.createElement('canvas');
      canvas.width = imageData.width;
      canvas.height = imageData.height;
      canvas.style['z-index'] = 5;
      canvas.getContext('2d').putImageData(imageData, 0, 0);
      explorer.append(canvas);
    }
  }
};
</script>


<style lang="scss">
#mosaic-container {
  position: relative;
  height: 250px;
  width: 500px;
  margin: 5px 20px;
}
</style>
