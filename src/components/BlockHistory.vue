<template>
  <div style="border: 1px solid #434; box-sizing: border-box">
    <svg ref="svg"></svg>
  </div>
</template>

<script>
import { ref } from 'vue';
import _ from 'lodash';
import * as d3 from 'd3';

export default {
  props: {
    blocks: {
      type: Array
    },
    seedIndex: {
      type: Number
    }
  },
  setup() {
    const svg = ref(null);
    return { svg };
  },
  emits: [
    'range-changed'
  ],
  watch: {
    seedIndex(n) {
      if (n === null) return;
      this.moveTo(n);
    }
  },
  mounted() {
    this.refresh();
  },
  methods: {
    refresh() {
      this.groupedBlocks = _.groupBy(this.blocks, d => {
        const t = d.created_at.split('-');
        return t[0] + '-' + t[1];
      });
      this.createTimeline(this.groupedBlocks);
    },
    moveTo(index) {
      const brush = this.brush;
      const x = this.x;

      let gIdx = 0;
      const values = Object.values(this.groupedBlocks);
      const id = this.blocks[index].id;

      for (let i = 0; i < values.length; i++) {
        if (_.some(values[i], d => d.id === id)) {
          gIdx = i;
          break;
        }
      }
      const start = Math.max(0, gIdx - 2);
      const end = Math.min(gIdx + 2, this.blocks.length - 1);

      d3.select('.brush').call(brush.move, [start, end].map(x));
    },
    createTimeline(groupedBlocks) {
      const keys = Object.keys(groupedBlocks);
      const values = Object.values(groupedBlocks);

      const margin = ({ top: 10, right: 30, bottom: 20, left: 30 });
      const width = 1000;
      const height = 90;

      const svg = d3.select(this.svg)
        .attr('viewBox', [0, 0, width, height]);

      const brushEnded = (event) => {
        const selection = event.selection;
        const [x0, x1] = selection.map(x.invert);

        const start = values[Math.floor(x0)][0].idx;
        const end = values[Math.floor(x1)][0].idx;

        this.$emit('range-changed', [start, end]);
      };
      this.brush = d3.brushX()
        .extent([[margin.left, margin.top], [width - margin.right, height - margin.bottom]])
        .on('start brush', brushed)
        .on('end', brushEnded);
      const brush = this.brush;

      this.x = d3.scaleLinear([0, keys.length - 1], [margin.left, width - margin.right]);
      const x = this.x;
      this.xAxis = g => g
        .attr('transform', `translate(0, ${height - margin.bottom})`)
        .call(d3.axisBottom(x).tickValues([0, Math.floor(keys.length / 2), keys.length - 1]).tickFormat(d => {
          return keys[d];
        }));
      const xAxis = this.xAxis;

      svg.append('g').call(xAxis);

      // Remove ticks
      svg.selectAll('.tick').selectAll('line').remove();
      svg.selectAll('.domain').remove();

      const bw = x(1) - x(0);
      const f = 0.17;

      svg.append('g')
        .selectAll('rect')
        .data(values)
        .join('rect')
        .attr('transform', (d, i) => {
          return `translate(${x(i)}, 0)`;
        })
        .attr('x', 0)
        .attr('y', d => {
          return 70 - f * d.length;
        })
        .attr('width', bw)
        .attr('height', d => f * d.length)
        .attr('fill', '#4b7');

      svg.append('g')
        .classed('brush', true)
        .call(brush)
        .call(brush.move, [0, 5].map(x))
        .call(g => g.select('.overlay')
          .datum({ type: 'selection' })
          .on('mousedown touchstart', beforebrushstarted)
        );

      function brushed(event) {
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
