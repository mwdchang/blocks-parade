<template>
  <div style="display:flex; flex-direction: column; justify-content: space-evenly">
    <h3>Bl.ocks Parade
      <small style="display:inline-flex; justify-content: center; align-items: center; background: #DDD">
        &nbsp;
        <img height="16" width="16" src="https://cdn.jsdelivr.net/npm/simple-icons@v4/icons/github.svg" />
        &nbsp;
        <a style="text-decoration: inherit" href="https://github.com/mwdchang/blocks-parade" target="_blank">
         Source
        </a>
        &nbsp;
      </small>
    </h3>
    <div style="padding: 0 40px; font-size: 85%; margin-top: 10px">
      Let's celebrating 10 years of D3.js by taking a stroll down memory lane and rediscover your favourite bl.ocks.
      Start by using the range slider below to select a time range.
    </div>
    <div v-if="blocks.length > 0" style="padding: 0 40px; font-size: 85%; margin-top: 5px; margin-bottom: 5px">
      Or start with one of these examples:
      <div class="button" @click="seed(4161)" style="display: inline-flex; padding: 5px 5px">
        <img :src="blocks[4161].thumbnail" width="46" height="24" />
      </div>
      <div class="button" @click="seed(255)" style="display: inline-flex; padding: 5px 5px">
        <img :src="blocks[255].thumbnail" width="46" height="24" />
      </div>
      <div class="button" @click="seed(500)" style="display: inline-flex; padding: 5px 5px">
        <img :src="blocks[500].thumbnail" width="46" height="24" />
      </div>
      <div class="button" @click="seed(4305)" style="display: inline-flex; padding: 5px 5px">
        <img :src="blocks[4305].thumbnail" width="46" height="24" />
      </div>
      <div class="button" @click="seed(4124)" style="display: inline-flex; padding: 5px 5px">
        <img :src="blocks[4124].thumbnail" width="46" height="24" />
      </div>
      <div class="button" @click="seed(4266)" style="display: inline-flex; padding: 5px 5px">
        <img :src="blocks[4266].thumbnail" width="46" height="24" />
      </div>
      <div class="button" @click="seed(10104)" style="display: inline-flex; padding: 5px 5px">
        <img :src="blocks[10104].thumbnail" width="46" height="24" />
      </div>
      <div class="button" @click="seed(6164)" style="display: inline-flex; padding: 5px 5px">
        <img :src="blocks[6164].thumbnail" width="46" height="24" />
      </div>
      <!--<div class="button" @click="seed(2)">#2</div> -->
    </div>
    <BlockHistory
      v-if="blocks.length > 0"
      style="margin-top: 5px"
      :seedIndex="seedIndex"
      :blocks="blocks"
      @range-changed="rangeChanged"/>
    <p style="padding: 0 40px">
      There are <span style="font-size: 150%">{{ numBlocksInRange }}</span> bl.ocks in your selected time range!!<br>
    </p>
    <Mosaic
      v-if="blocks.length > 0 && targetIndex !== null"
      :targetIndex="targetIndex"
      :range="[start, end]"
      :blocks="blocks"
      @shuffle="shuffle"
      @error="error"
      @working="working"
      @ready="ready" />
    <div v-if="showOverlay"
      class="overlay">
      <div class="lds-grid"><div></div><div></div><div></div><div></div><div></div><div></div><div></div><div></div><div></div>
      </div>
      Creating mosaic <br>
    </div>
  </div>
</template>

<script>
import { ref } from 'vue';
import BlockHistory from './components/BlockHistory.vue';
import Mosaic from './components/Mosaic.vue';
import * as data from './assets/cleaned.json';

export default {
  name: 'App',
  components: {
    // eslint-disable-next-line
    BlockHistory, Mosaic
  },
  setup() {
    const blocks = ref([]);
    const showOverlay = ref(false);
    const showError = ref(false);
    const targetIndex = ref(null);
    const seedIndex = ref(null);
    const numBlocksInRange = ref(0);
    const start = ref(0);
    const end = ref(1);
    window.blocks = blocks;

    return {
      blocks,
      targetIndex,
      seedIndex,
      showOverlay,
      showError,
      numBlocksInRange,
      start,
      end
    };
  },
  computed: {
    targetBlock() {
      return this.blocks[this.targetIndex];
    }
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
      // this.showOverlay = true;
      this.showError = false;
      const [start, end] = range.map(Math.floor);
      this.start = start;
      this.end = end;

      this.numBlocksInRange = (end - start) + 1;

      if (this.seedIndex) {
        this.targetIndex = this.seedIndex;
      } else {
        this.targetIndex = Math.floor(start + Math.random() * (end - start));
      }
      this.seedIndex = null;
    },
    shuffle() {
      const start = this.start;
      const end = this.end;
      this.targetIndex = Math.floor(start + Math.random() * (end - start));
      this.seedIndex = null;
    },
    seed(num) {
      if (this.seedIndex === num) return;
      // this.showOverlay = true;
      this.seedIndex = num;
    },
    ready() {
      this.showOverlay = false;
    },
    error() {
      this.showError = true;
      this.showOverlay = false;
    },
    working() {
      this.showOverlay = true;
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

.button {
  display: inline-block;
  border-radius: 5px;
  background: #369;
  padding: 2px;
  font-size: 85%;
  margin: 0 2px;
  padding: 3px 7px;
  cursor: pointer;
  min-width: 25px;
}

.button:hover {
  opacity: 0.75;
}
</style>
