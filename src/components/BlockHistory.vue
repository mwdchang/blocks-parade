<template>
  <div>
    <svg ref="block"></svg>
  </div>
</template>

<script>
import { ref, onMounted } from 'vue';
import * as d3 from 'd3';

function test(el) {
  d3.select(el)
    .append('circle')
    .attr('cx', 50)
    .attr('cy', 50)
    .attr('r', 20)
    .attr('fill', '#f80');
}

export default {
  setup() {
    const block = ref(null);
    onMounted(() => {
      test(block.value);
    });

    return {
      block
    };
  }
};
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped lang="scss">
h3 {
  margin: 40px 0 0;
}
ul {
  list-style-type: none;
  padding: 0;
}
li {
  display: inline-block;
  margin: 0 10px;
}
a {
  color: #42b983;
}
</style>
