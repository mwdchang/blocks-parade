<template>
  <h3>Blocks Parade
    <small style="display:inline-flex; align-items: center; background: #DDD">
      &nbsp;
      <img height="16" width="16" src="https://cdn.jsdelivr.net/npm/simple-icons@v4/icons/github.svg" />
      &nbsp;
      <a href="https://github.com/mwdchang/blocks-parade">
       Source
      </a>
      &nbsp;
    </small>
  </h3>
  <p style="padding: 0 40px">
    Celebrating 10 years of D3 by taking a stroll down memory lane and rediscover your favourite blocks. Start by using the time slider below to select a sampling range.
    <br>
    Examples:
    <button @click="seed(1808)">1808</button>
    <button @click="seed(500)">500</button>
  </p>
  <BlockHistory
    v-if="blocks.length > 0"
    :seedIndex="seedIndex"
    :blocks="blocks"
    @range-changed="rangeChanged"/>
  <p style="padding: 0 40px">
    Other blocks in the time range wil be used as tiles to create a moasica in the likeliness of the chosen block.
    Hover over the tiles to see a larger version, click on the tiles to view them on http://bl.ocks.org/
  </p>
  <Mosaic
    v-if="blocks.length > 0"
    :targetIndex="targetIndex"
    :blocks="blocks"
    @ready="ready" />
  <div v-if="showOverlay"
    class="overlay">
    <div class="lds-grid"><div></div><div></div><div></div><div></div><div></div><div></div><div></div><div></div><div></div>
    </div>
    Computing mosaic
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
    const seedIndex = ref(null);

    return {
      blocks,
      targetIndex,
      seedIndex,
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
    seed(num) {
      this.showOverlay = true;
      this.seedIndex = num;
      this.targetIndex = num;
      console.log('seeding', num);
    },
    ready() {
      this.showOverlay = false;
    }
  }
};
</script>

<style lang="scss">

body {
  background: #112;
}

h3 {
  margin: 0 10px;
}

p, h3, div {
  color: #EEE2EE;
}

small {
  border-radius: 2px;
}

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
  opacity: 0.6;
  display: flex;
  justify-content: center;
  align-items: center;
  font-size: 225%;
  color: #222;
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

p {
  font-size: 85%;
}
</style>
