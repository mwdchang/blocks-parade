<template>
  <div>
    <svg ref="svg"></svg>
  </div>
</template>

<script>
import { ref } from 'vue';
import _ from 'lodash';
import * as d3 from 'd3';

/*
function test(el) {
  d3.select(el)
    .append('circle')
    .attr('cx', 50)
    .attr('cy', 50)
    .attr('r', 20)
    .attr('fill', '#f80');
}
*/

export default {
  props: {
    blocks: {
      type: Array
    }
  },
  setup() {
    const svg = ref(null);
    return { svg };
  },
  emits: [
    'range-changed'
  ],
  mounted() {
    this.refresh();
  },
  methods: {
    refresh() {
      const groupedBlocks = _.groupBy(this.blocks, d => {
        const t = d.created_at.split('-');
        return t[0] + '-' + t[1];
      });
      this.createTimeline(groupedBlocks);
    },
    createTimeline(groupedBlocks) {
      const keys = Object.keys(groupedBlocks);
      const values = Object.values(groupedBlocks);

      const margin = ({ top: 20, right: 20, bottom: 20, left: 20 });
      const width = 1000;
      const height = 100;

      const svg = d3.select(this.svg)
        .attr('viewBox', [0, 0, width, height]);

      const brushEnded = (event) => {
        const selection = event.selection;
        const [x0, x1] = selection.map(x.invert);

        const start = values[Math.floor(x0)][0].idx;
        const end = values[Math.floor(x1)][0].idx;

        this.$emit('range-changed', [start, end]);
      };
      const brush = d3.brushX()
        .extent([[margin.left, margin.top], [width - margin.right, height - margin.bottom]])
        .on('start brush', brushed)
        .on('end', brushEnded);

      const x = d3.scaleLinear([0, keys.length - 1], [margin.left, width - margin.right]);
      const xAxis = g => g
        .attr('transform', `translate(0, ${height - margin.bottom})`)
        .call(d3.axisBottom(x).tickValues([0, Math.floor(keys.length / 2), keys.length - 1]).tickFormat(d => {
          return keys[d];
        }));

      svg.append('g').call(xAxis);

      // Remove ticks
      svg.selectAll('.tick').selectAll('line').remove();
      svg.selectAll('.domain').remove();

      svg.append('g')
        .attr('fill-opacity', 0.2)
        .selectAll('circle')
        .data(values)
        .join('circle')
        .attr('transform', (d, i) => {
          return `translate(${x(i)}, 50)`;
        })
        .attr('r', d => {
          return Math.sqrt(d.length);
        });

      svg.append('g')
        .call(brush)
        .call(brush.move, [0, 5].map(x))
        .call(g => g.select('.overlay')
          .datum({ type: 'selection' })
          .on('mousedown touchstart', beforebrushstarted)
        );



      function brushed(event) {
        const selection = event.selection;
        if (selection === null) {
          // circle.attr('stroke', null);
        } else {
          // const [x0, x1] = selection.map(x.invert);
          // circle.attr('stroke', d => x0 <= d && d <= x1 ? 'red' : null);
        }
      }

      function beforebrushstarted(event) {
        const dx = x(1) - x(0); // Use a fixed width when recentering.
        const [[cx]] = d3.pointers(event);
        const [x0, x1] = [cx - dx / 2, cx + dx / 2];
        const [X0, X1] = x.range();
        d3.select(this.parentNode)
          .call(brush.move, x1 > X1 ? [X1 - dx, X1]
            : x0 < X0 ? [X0, X0 + dx] : [x0, x1]);
      }
    }
  }
};
</script>

<style scoped lang="scss">
svg {
  /deep/ .tick {
    opacity: 0.5;
  }
}
</style>
