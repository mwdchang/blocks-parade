<template>
  <p>Blocks Parade: Celebrating 10 years of D3</p>
  <Mosaic
    v-if="blocks.length > 0"
    :targetIndex="targetIndex"
    :blocks="blocks" />
  <BlockHistory
    v-if="blocks.length > 0"
    :blocks="blocks" />
</template>

<script>
import { ref } from 'vue';
import BlockHistory from './components/BlockHistory.vue';
import Mosaic from './components/Mosaic.vue';
import * as data from './assets/cleaned.json';

// const TARGET_INDEX = 55;
const TARGET_INDEX = 255;

export default {
  name: 'App',
  components: {
    BlockHistory, Mosaic
  },
  setup() {
    const blocks = ref([]);
    const targetIndex = ref(TARGET_INDEX);
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
      this.blocks = blocks;
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
