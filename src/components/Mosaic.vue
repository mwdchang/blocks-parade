<template>
    <div>
      <div style="font-size: 125%; background: #798"
        class="button"
        @click="shuffle()">Shuffle Image</div>
      &nbsp;
      <div style="font-size: 125%"
        class="button"
        @click="createMosaic()">Create Mosaic !!</div>
    </div>

  <div style="display: flex; padding: 10px 10px; justify-content: center">
    <div style="width: 320px; font-size: 85%">
      <div v-if="showError === false">{{ targetBlock.description }} {{ targetBlock.idx }}</div>
      <div
        v-if="showError === false"
        id="target-container">
      </div>
      <div v-if="showError === true">
        <div style="font-size: 150%; color: #F60">
          Oops! We cannot find the image for block {{targetBlock.id}}, the data may have been changed or removed :(
          <br>Please try a different block.
        </div>
      </div>
      <div v-if="showError === false"><em><strong>{{ targetBlock.userId }}</strong></em></div>
      <div v-if="showError === false && targetBlock.created_at">{{ targetBlock.created_at.split('T')[0] }} </div>
    </div>
    <div id="mosaic-container"></div>
    <div style="width: 320px; font-size: 85%">
      <div>{{ exploreBlock.description }} </div>
      <div id="explorer-container"></div>
      <div><em><strong>{{ exploreBlock.userId }}</strong></em></div>
      <div v-if="exploreBlock.created_at">{{ exploreBlock.created_at.split('T')[0] }} </div>
    </div>
  </div>
</template>

<script>

import _ from 'lodash';
import * as d3 from 'd3';
import ImageUtil from '../libs/image-util';

const BASE_W = 230;
const BASE_H = 120;

const TARGET_W = BASE_W * 2.0;
const TARGET_H = BASE_H * 2.0;

const TILE_W = 23;
const TILE_H = 12;

// eslint-disable-next-line
const DURATION = 3600;

// eslint-disable-next-line
const SAMPLE_RANGE = 25;

const imageCache = new Map();

// eslint-disable-next-line
async function loadThumbnail(blocks, startIdx, endIdx, width, height) {
  // FIXME use web-workers to speed it up, or preprocess
  const r = [];
  for (let i = startIdx; i <= endIdx; i++) {
    if (blocks[i].imageData) {
      r.push(blocks[i]);
      continue;
    }

    try {
      const d = await ImageUtil.loadImage(blocks[i].thumbnail, { width, height });
      if (!_.isNil(d)) {
        blocks[i].imageData = d;
        r.push(blocks[i]);
      }
    } catch (err) {
      // blocks[i].imageData = null;
    }
  }
  return r;
}

// eslint-disable-next-line
async function loadThumbnailsInRange(blocks, range, width, height) {
  // FIXME use web-workers to speed it up, or preprocess
  const r = [];
  for (let i = 0; i < range.length; i++) {
    const idx = range[i];

    if (blocks[idx].imageData) {
      r.push(blocks[idx]);
      continue;
    }

    try {
      const d = await ImageUtil.loadImage(blocks[idx].thumbnail, { width, height });
      if (!_.isNil(d)) {
        blocks[idx].imageData = d;
        r.push(blocks[idx]);
      }
    } catch (err) {
      // blocks[i].imageData = null;
    }
  }
  return r;
}



async function loadOne(blocks, idx, width, height) {
  const d = await ImageUtil.loadImage(blocks[idx].thumbnail, { width, height });
  return d;
}

// eslint-disable-next-line
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
    },
    range: {
      type: Array
    }
  },
  data: () => ({
    targetBlock: {},
    exploreBlock: {},
    showError: false
  }),
  emits: ['ready'],
  watch: {
    targetIndex(n) {
      if (n) {
        this.refresh();
      }
    }
  },
  mounted() {
    this.refresh();
  },
  methods: {
    async refresh() {
      const blocks = this.blocks;
      const targetIndex = this.targetIndex;

      this.collapseTiles();
      d3.select('#target-container').selectAll('*').remove();
      d3.select('#explorer-container').selectAll('*').remove();
      this.exploreBlock = {};

      // Load a random target
      let target = null;
      try {
        target = await loadOne(blocks, targetIndex, 230, 120);
      } catch {
        this.showError = true;
        this.$emit('error');
        return;
      }

      this.targetBlock = blocks[targetIndex];
      // console.log('target block', this.targetBlock);
      const canvas = document.createElement('canvas');
      canvas.width = target.width;
      canvas.height = target.height;
      canvas.style['z-index'] = 5;

      canvas.getContext('2d').putImageData(target, 0, 0);
      document.getElementById('target-container').append(canvas);

      // Make the target image 2X larger to better git
      const canvas2 = document.createElement('canvas');
      canvas2.id = 'target-image';
      canvas2.width = TARGET_W;
      canvas2.height = TARGET_H;
      const ctx2 = canvas2.getContext('2d');
      ctx2.drawImage(canvas, 0, 0, TARGET_W, TARGET_H);
      this.targetImageData2X = ctx2.getImageData(0, 0, TARGET_W, TARGET_H);
      this.$emit('ready');
    },
    async collapseTiles() {
      d3.select('#mosaic-container').select('.help-text').remove();
      d3.select('#mosaic-container').selectAll('.tile2').classed('tile2', false).each(function() {
        d3.select(this).transition().duration(800 + Math.random() * 200).style('top', 270 + Math.random() * 500 + 'px').remove();
      });
    },
    async shuffle() {
      this.showError = false;
      this.$emit('shuffle');
    },
    async createMosaic() {
      console.log(this.range);

      const indices = [];
      for (let i = this.range[0]; i <= this.range[1]; i++) {
        indices.push(i);
      }
      const shuffled = _.take(_.shuffle(indices), 50);
      // console.log(shuffled);

      // return;
      this.$emit('working');
      this.collapseTiles();
      // d3.select('#mosaic-container').selectAll('*').remove();
      d3.select('#explorer-container').selectAll('*').remove();

      const blocks = this.blocks;

      // 1. Load source images
      // const start = Math.floor(Math.max(0, this.targetIndex - 25));
      // const end = Math.floor(Math.min(blocks.length - 1, this.targetIndex + 25));

      const availableBlocks = await loadThumbnailsInRange(blocks, shuffled, TILE_W, TILE_H);
      const sourceImages = [];
      for (let i = 0; i < availableBlocks.length; i++) {
        const b = availableBlocks[i];
        sourceImages.push(b);
      }

      // 2. Chop and run best matching tile
      // FIXME: Split into web-worker threads
      const bestTiles = [];
      for (let i = 0; i < (TARGET_W / TILE_W); i++) {
        for (let j = 0; j < (TARGET_H / TILE_H); j++) {
          const tile = ImageUtil.crop(this.targetImageData2X.data,
            { width: TARGET_W, height: TARGET_H, channels: 4 },
            { x: i * TILE_W, y: j * TILE_H, width: TILE_W, height: TILE_H }
          );
          const best = findBestImage(sourceImages, tile);
          bestTiles.push({
            tile: best,
            left: i * TILE_W,
            top: j * TILE_H
          });
        }
      }
      this.$emit('ready');

      // Animate in
      d3.select('#mosaic-container')
        .selectAll('.tile2')
        .data(bestTiles)
        .enter()
        .append('canvas')
        .attr('class', () => {
          const r = Math.random();
          if (r < 0.33) {
            return 'tile2 flip-z';
          } else if (r < 0.66) {
            return 'tile2 flip-y';
          }
          return 'tile2';
        })
        .style('position', 'absolute')
        .style('opacity', 1.0)
        .style('border', '1px solid #434')
        .style('left', () => (Math.random() * 2000 - 1000) + 'px')
        .style('top', () => (Math.random() * 2000 - 1000) + 'px')
        .style('cursor', 'pointer')
        .attr('width', TILE_W + 'px')
        .attr('height', TILE_H + 'px')
        .on('mouseover', (event, d) => {
          this.showTile(d.tile);
        })
        .on('click', (event, d) => {
          window.open(`http://bl.ocks.org/${d.tile.userId}/${d.tile.id}`, '_blank');
        })
        .each(function(d) {
          const canvas = d3.select(this).node();
          drawRGBA(canvas.getContext('2d'), d.tile.imageData.data, TILE_W, TILE_H);
        });

      await d3.selectAll('.tile2')
        .transition()
        .duration(DURATION)
        .style('left', d => d.left + 'px')
        .style('top', d => d.top + 'px')
        .end();

      d3.selectAll('.tile2').classed('flip-z', false).classed('flip-y', false);
      d3.select('#mosaic-container').append('div')
        .classed('help-text', true)
        .style('position', 'absolute')
        .style('top', '260px')
        .style('font-size', '85%')
        .text('Hover on tiles to see previews, click on tiles to go to the original bl.ocks');
    },
    async showTile(tile) {
      this.exploreBlock = tile;
      let imageData = null;
      if (imageCache.has(tile.id)) {
        imageData = imageCache.get(tile.id);
      } else {
        imageData = await ImageUtil.loadImage(tile.thumbnail, { width: BASE_W, height: BASE_H });
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
  margin: 0px 20px;
}

#target-container {
  min-height: 120px
}


.flip-z {
  animation: z-rotate 1.8s both infinite;
}

.flip-y {
  animation: y-rotate 1.8s both infinite;
}


@keyframes z-rotate {
  0 {
    transform: rotateZ(0);
  }
  50% {
    transform: rotateZ(180deg);
  }
  100% {
    transform: rotateZ(359deg);
  }
}

@keyframes y-rotate {
  0 {
    transform: rotateY(0);
  }
  50% {
    transform: rotateY(180deg);
  }
  100% {
    transform: rotateY(0deg);
  }
}
</style>
