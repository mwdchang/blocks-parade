<template>
  <div> Mosiac </div>
</template>

<script>
export default {
  props: {
    blocks: {
      type: Array
    }
  },
  mounted() {
    this.refresh();
  },
  methods: {
    async refresh() {
    }
  }
};
</script>

