<template>
  <BlockHistory
    v-if="blocks.length > 0"
    :blocks="blocks" />
</template>

<script>
import * as d3 from 'd3';
import { ref } from 'vue';
import BlockHistory from './components/BlockHistory.vue';
import * as data from './assets/cleaned.json';
import ImageUtil from './libs/image-util';


const BASE_W = 230;
const BASE_H = 120;

const TARGET_W = BASE_W * 2.0;
const TARGET_H = BASE_H * 2.0;

const TILE_W = 46;
const TILE_H = 24;


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

/*
const findBestImage = (sourceImages, target) => {
  let r = sourceImages[0];
  let dist = 999999999;
  for (let i = 0; i < sourceImages.length; i++) {
    const d = ImageUtil.distance(target, sourceImages[i].data);
    if (d < dist) {
      dist = d;
      r = sourceImages[i];
    }
  }
  return r;
};
*/

const drawRGBA = (ctx, data, w, h, x = 0, y = 0) => {
  const imageData = ctx.createImageData(w, h);
  for (let i = 0; i < data.length; i++) {
    const v = data[i];
    imageData.data[i] = v;
  }
  ctx.putImageData(imageData, x, y);
};



export default {
  name: 'App',
  components: {
    BlockHistory
  },
  setup() {
    const blocks = ref([]);
    return {
      blocks
    };
  },
  mounted() {
    this.refresh();
  },
  methods: {
    async refresh() {
      const blocks = data.default;
      this.blocks = blocks;

      // Load a random target
      const target = (await loadThumbnail(blocks, 40, 40, 230, 120))[0];

      const canvas = document.createElement('canvas');
      canvas.width = target.imageData.width;
      canvas.height = target.imageData.height;
      canvas.getContext('2d').putImageData(target.imageData, 0, 0);

      // Make the target image 2X larger to better git
      const canvas2 = document.createElement('canvas');
      canvas2.id = 'target-image';
      canvas2.width = TARGET_W;
      canvas2.height = TARGET_H;
      const ctx2 = canvas2.getContext('2d');
      ctx2.drawImage(canvas, 0, 0, TARGET_W, TARGET_H);
      // document.body.append(canvas2);
      const targetImageData2X = ctx2.getImageData(0, 0, TARGET_W, TARGET_H);

      // 1. Load source images
      // const availableBlocks = await loadThumbnail(blocks, 40, 50, TILE_W, TILE_H);
      // for (let i = 0; i < availableBlocks.length; i++) {
      //   const b = availableBlocks[i];
      //   const canvas = document.createElement('canvas');
      //   canvas.width = b.imageData.width;
      //   canvas.height = b.imageData.height;
      //   canvas.getContext('2d').putImageData(b.imageData, 0, 0);
      //   document.body.append(canvas);
      // }

      // 2. Chop and run best matching tile
      // FIXME: Split into web-worker threads
      document.body.append(document.createElement('br'));

      for (let i = 0; i < (TARGET_W / TILE_W); i++) {
        for (let j = 0; j < (TARGET_H / TILE_H); j++) {
          const tile = ImageUtil.crop(targetImageData2X.data,
            { width: TARGET_W, height: TARGET_H, channels: 4 },
            { x: i * TILE_W, y: j * TILE_H, width: TILE_W, height: TILE_H } // reverse W and H
          );

          const canvas = document.createElement('canvas');
          canvas.width = TILE_W;
          canvas.height = TILE_H;
          drawRGBA(canvas.getContext('2d'), tile, TILE_W, TILE_H);
          document.body.append(canvas);
          // canvas.getContext('2d').putImageData(blah, 0, 0);

          d3.select(canvas)
            .style('position', 'absolute')
            .style('left', (Math.random() * 2000 - 1000) + 'px')
            .style('top', (Math.random() * 2000 - 1000) + 'px')
            .transition()
            .duration(2000)
            .style('left', 100 + i * TILE_W + 'px')
            .style('top', 100 + j * TILE_H + 'px');
        }
        document.body.append(document.createElement('br'));
      }
    }
  }
};
</script>

<style lang="scss">
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  margin-top: 60px;
}
</style>
