<template>
  <div class="offset-infos">
    <span>hello</span>
    <div class="offset-list">
      <div
        v-for="(data, index) in offsetInfos"
        :key="data.id"
        class="offset-data"
        :class="{ first: index === 0, last: index === offsetInfos.length - 1 }"
        @xmousedown="handleMouseDown(index, $event)"
        @xmousemove="handleMouseMove(index, $event)"
        @xmouseup="handleMouseUp(index, $event)"
      >
        <div class="data-section">
          <select v-model="data.type">
            <option value="type1">KAO</option>
            <option value="type2">GRP</option>
            <option value="type3">NPK</option>
          </select>
          <label>Offset:</label>
          <input type="number" v-model.number="data.offset" />
          <label>Size:</label>
          <input type="number" v-model.number="data.size" />
        </div>
        <div class="action-section">
          <button class="delete-btn" @click="handleDelete(index)">
            Delete
          </button>
        </div>
      </div>
    </div>
    <div class="add-section">
      <button @click="handleAdd">Add Offset Data</button>
    </div>
    <div class="apply-section">
      <button @click="handleApply">Apply Offset Data</button>
    </div>
  </div>
</template>

<script>
export default {
  name: 'OffsetInfos',
  data () {
    return {
      offsetInfos: [{ id: 1, type: 'type1', offset: 0, size: 1 }],
      isDragging: false,
      dragStartIndex: null,
      dragEndIndex: null
    }
  },
  methods: {
    handleAdd () {
      const newId = this.offsetInfos.length + 1
      this.offsetInfos.push({ id: newId, type: 'type1', offset: 0, size: 1 })
    },
    handleApply () {},
    handleDelete (index) {
      if (this.offsetInfos.length === 1) {
        alert('Cannot delete the only offset data')
        return
      }
      this.offsetInfos.splice(index, 1)
    },
    // handleMouseDown (index, event) {
    //   this.isDragging = true
    //   this.dragStartIndex = index
    //   event.preventDefault()
    // },
    // handleMouseMove (index, event) {
    //   if (!this.isDragging) {
    //     return
    //   }
    //   this.dragEndIndex = index
    //   this.swapData()
    //   event.preventDefault()
    // },
    // handleMouseUp (index, event) {
    //   this.isDragging = false
    //   this.dragStartIndex = null
    //   this.dragEndIndex = null
    //   event.preventDefault()
    // },
    swapData () {
      if (this.dragStartIndex === null || this.dragEndIndex === null) {
        return
      }
      const temp = this.offsetInfos[this.dragStartIndex]
      this.offsetInfos.splice(this.dragStartIndex, 1)
      this.offsetInfos.splice(this.dragEndIndex, 0, temp)
    }
  }
}
</script>

<style>
.offset-infos {
  display: flex;
  flex-direction: column;
  gap: 10px;
  padding: 10px;
}
.offset-data {
  display: flex;
  justify-content: space-between;
  gap: 10px;
  padding: 10px;
  border: 1px solid #ccc;
  border-radius: 5px;
  background-color: #f5f5f5;
}
.offset-data.first {
  border-top: none;
}
.offset-data.last {
  border-bottom: none;
}
.offset-data .data-section {
  display: flex;
  gap: 10px;
  align-items: center;
}
.offset-data .action-section {
  display: flex;
  gap: 10px;
  align-items: center;
}
.add-section button {
  padding: 5px;
  border-radius: 5px;
  background-color: #4caf50;
  color: #fff;
  border: none;
}
.apply-section button {
  padding: 5px;
  border-radius: 5px;
  background-color: orchid;
  color: #fff;
  border: none;
}
.delete-btn {
  padding: 5px;
  border-radius: 5px;
  background-color: #f44336;
  color: #fff;
  border: none;
}
</style>
