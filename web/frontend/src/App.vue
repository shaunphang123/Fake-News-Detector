<template>
<v-app>
    <v-main>
        <v-card>
            <v-layout>
                <NavigationDrawerComponent/>
                <PredictionComponent/>
            </v-layout>
        </v-card>
    </v-main>
</v-app>
</template>

<script setup>
import PredictionComponent from './components/PredictionComponent.vue';
</script>
