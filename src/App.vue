<template>
  <p>Blocks Parade: Celebrating 10 years of D3</p>
  <Mosaic
    v-if="blocks.length > 0"
    :targetIndex="targetIndex"
    :blocks="blocks" />
  <BlockHistory
    v-if="blocks.length > 0"
    :blocks="blocks"
    @range-changed="rangeChanged"/>
</template>

<script>
import { ref } from 'vue';
import BlockHistory from './components/BlockHistory.vue';
import Mosaic from './components/Mosaic.vue';
import * as data from './assets/cleaned.json';

// const TARGET_INDEX = 15;
// const TARGET_INDEX = 55;
// const TARGET_INDEX = 255;
// const TARGET_INDEX = 1833;
// const TARGET_INDEX = 500;

export default {
  name: 'App',
  components: {
    BlockHistory, Mosaic
  },
  setup() {
    const blocks = ref([]);
    const targetIndex = ref(null);
    return {
      blocks,
      targetIndex
    };
  },
  mounted() {
    this.refresh();
  },
  methods: {
    async refresh() {
      const blocks = data.default;
      blocks.forEach((b, i) => {
        b.idx = i;
      });
      this.blocks = blocks;
    },
    rangeChanged(range) {
      const [start, end] = range.map(Math.floor);

      this.targetIndex = Math.floor(start + Math.random() * (end - start));
      console.log('range', start, end);
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
}
</style>
