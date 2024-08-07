<script>
export default {
    setup() {
        const pastPredictions = JSON.parse(localStorage.getItem('pastPredictions'))
        return { pastPredictions }
    },
    
}
</script>
<template>
    <v-navigation-drawer
        expand-on-hover
        rail
    >
        <v-list density="compact" nav>
            <v-tooltip v-for="pastPrediction in pastPredictions" :text="`${(parseFloat(pastPrediction.prediction_score * 100)).toFixed(2)}% certainty that this is fake news`">
                <template v-slot:activator="{ props }">
                    <v-list-item :key="pastPrediction.article" prepend-icon="mdi-book-alphabet" value="starred" v-bind="props">
                        <v-list-item-title>{{ pastPrediction.article }}</v-list-item-title>
                        <v-list-item-subtitle>{{ pastPrediction.prediction }}</v-list-item-subtitle>
                    </v-list-item>
                </template>
            </v-tooltip>
        </v-list>
    </v-navigation-drawer>
</template>