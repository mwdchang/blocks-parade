<template>
  <h3>Blocks Parade</h3>
  <p style="padding: 0 40px">
    We celebrating 10 years of D3 by taking a stroll down memory lane and rediscover our favourite blocks.
    As you change the selected range on the time-slider, a random block will be selected within the time frame,
    then we will create a mosaic-tribute by recomposing the blocks by its neighouring blocks.
  </p>
  <Mosaic
    v-if="blocks.length > 0"
    :targetIndex="targetIndex"
    :blocks="blocks"
    @ready="ready" />
  <BlockHistory
    v-if="blocks.length > 0"
    :blocks="blocks"
    @range-changed="rangeChanged"/>
  <div v-if="showOverlay"
    class="overlay">
    <div class="lds-grid"><div></div><div></div><div></div><div></div><div></div><div></div><div></div><div></div><div></div>
    </div>
    Loading...
  </div>
</template>

<script>
import { ref } from 'vue';
import BlockHistory from './components/BlockHistory.vue';
import Mosaic from './components/Mosaic.vue';
import * as data from './assets/cleaned.json';

// works nicely with mosaic
// const TARGET_INDEX = 1808;
// const TARGET_INDEX = 15;
// const TARGET_INDEX = 55;
// const TARGET_INDEX = 255;
// const TARGET_INDEX = 1833;
// const TARGET_INDEX = 500;

export default {
  name: 'App',
  components: {
    // eslint-disable-next-line
    BlockHistory, Mosaic
  },
  setup() {
    const blocks = ref([]);
    const showOverlay = ref(false);
    const targetIndex = ref(null);
    return {
      blocks,
      targetIndex,
      showOverlay
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
      this.showOverlay = true;
      const [start, end] = range.map(Math.floor);
      this.targetIndex = Math.floor(start + Math.random() * (end - start));
      console.log('range', start, end);
    },
    ready() {
      this.showOverlay = false;
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

.overlay {
  position: absolute;
  top: 0px;
  left: 0px;
  width: 100vw;
  height: 100vh;
  background: #eee;
  opacity: 0.5;
  display: flex;
  justify-content: center;
  align-items: center;
}

// see https://loading.io/css/
.lds-grid {
  display: inline-block;
  position: relative;
  width: 80px;
  height: 80px;
}
.lds-grid div {
  position: absolute;
  width: 16px;
  height: 16px;
  border-radius: 50%;
  background: #369;
  animation: lds-grid 1.2s linear infinite;
}
.lds-grid div:nth-child(1) {
  top: 8px;
  left: 8px;
  animation-delay: 0s;
}
.lds-grid div:nth-child(2) {
  top: 8px;
  left: 32px;
  animation-delay: -0.4s;
}
.lds-grid div:nth-child(3) {
  top: 8px;
  left: 56px;
  animation-delay: -0.8s;
}
.lds-grid div:nth-child(4) {
  top: 32px;
  left: 8px;
  animation-delay: -0.4s;
}
.lds-grid div:nth-child(5) {
  top: 32px;
  left: 32px;
  animation-delay: -0.8s;
}
.lds-grid div:nth-child(6) {
  top: 32px;
  left: 56px;
  animation-delay: -1.2s;
}
.lds-grid div:nth-child(7) {
  top: 56px;
  left: 8px;
  animation-delay: -0.8s;
}
.lds-grid div:nth-child(8) {
  top: 56px;
  left: 32px;
  animation-delay: -1.2s;
}
.lds-grid div:nth-child(9) {
  top: 56px;
  left: 56px;
  animation-delay: -1.6s;
}
@keyframes lds-grid {
  0%, 100% {
    opacity: 1;
  }
  50% {
    opacity: 0.5;
  }
}
</style>
