import { View, Text, TextInput, StyleSheet, Image, ScrollView, Button, TouchableOpacity, TouchableWithoutFeedback, Keyboard, BackHandler } from 'react-native'
import React, { useContext, useState, useEffect, useRef } from 'react'
import { SafeAreaView } from 'react-native-safe-area-context'
import { useNavigation } from '@react-navigation/native';
import * as Font from 'expo-font';
// import '../../index.css'

import Categories from '../../components/categories';
import { AuthContext } from '../../context/AuthContext';

// // Load the custom font
// async function loadCustomFont() {
//   await Font.loadAsync({
//     'YourCustomFontName': require('../../assets/fonts/Fuzzy Bubbles Regular.ttf'),
//   });
// }

// loadCustomFont();

export default function Home() {
  const { logout } = useContext(AuthContext);
  const navigation = useNavigation();

  const handleCardClick = (workerType) => {
    console.log("Type",workerType)
    navigation.navigate('WorkerInfo', { service:workerType });
  };


  return (
    // <TouchableWithoutFeedback onPress={handleOutsidePress}>
      <SafeAreaView className="bg-white">
        <ScrollView className='pt-4'>
          {/*main*/}

          <View
            horizontal
            showsVerticalScrollIndicator={false}
            className='pb-0'
          >
            {/* categories */}
            <Categories />

            {/* <Divider width={2} insetType="left"/> */}
            <Text  className='text-2xl mt-8 mx-5 font-ionicons'>Featured</Text>
            <View className='flex flex-row justify-around my-2'>
              <TouchableOpacity onPress={() => { navigation.navigate('WorkerInfo',{service:'Barber'}) }}>
                <View className='flex flex-col justify-center items-left ml-1'>
                  <Image className='w-20 h-20' source={require('../../assets/icons/Barber.png')} />
                  <Text className="ml-2 pr-4 text-center">Barber</Text>
                </View>
              </TouchableOpacity >
              <TouchableOpacity onPress={() => { navigation.navigate('WorkerInfo',{service:'Carpentry'}) }}>
              <View className='flex flex-col justify-center items-center'>
                <Image className='w-20 h-20' source={require('../../assets/icons/Carpenter.png')} />
                <Text>Carpentry</Text>
              </View>
              </TouchableOpacity >
              <TouchableOpacity onPress={handleCardClick}>
              <View className='flex flex-col justify-center items-center mr-1'>
                <Image className='w-20 h-20' source={require('../../assets/icons/electrician.png')} />
                <Text >Electrician</Text>
              </View>
              </TouchableOpacity >
            </View>
            <View className='flex flex-row justify-around mt-2'>
              <TouchableOpacity onPress={handleCardClick}>
                <View className='flex flex-col justify-center items-center ml-1'>
                  <Image className='w-20 h-20' source={require('../../assets/icons/House Cleaner.png')} />
                  <Text >House Cleaner</Text>
                </View>
              </TouchableOpacity>
              <TouchableOpacity onPress={handleCardClick}>
              <View className='flex flex-col justify-center items-center'>
                <Image className='w-20 h-20' source={require('../../assets/icons/Massage Therepist.png')} />
                <Text >Massage Therepy</Text>
              </View>
              </TouchableOpacity>
              <TouchableOpacity onPress={handleCardClick}>
              <View className='flex flex-col justify-center items-center mr-1'>
                <Image className='w-20 h-20' source={require('../../assets/icons/HVAC Technician.png')} />
                <Text >HVAC Technician</Text>
              </View>
              </TouchableOpacity>
            </View>
          </View>


          {/* ------------------------------------- */}

          <Text  className='text-2xl mt-10 mx-5 font-nunito-sans font-normal'>Top Problems</Text>

          <View className='flex flex-row justify-around mt-2'>
            <View className='flex flex-col justify-center items-center'>
              <Image className='w-16 h-16' source={require('../../assets/icons/Locksmith.png')} />
              <Text >Locksmith</Text>
            </View>
            <View className='flex flex-col justify-center items-center'>
              <Image className='w-16 h-16' source={require('../../assets/icons/manicure.png')} />
              <Text >Manicure</Text>
            </View>
            <View className='flex flex-col justify-center items-center'>
              <Image className='w-16 h-16' source={require('../../assets/icons/Hair care.png')} />
              <Text >Hair Care</Text>
            </View>
            <View className='flex flex-col justify-center items-center'>
              <Image className='w-16 h-16' source={require('../../assets/icons/Chef.png')} />
              <Text >Chef</Text>
            </View>
          </View>
          <View className='flex flex-row justify-around mt-2 mb-6'>
            <View className='flex flex-col justify-center items-center'>
              <Image className='w-16 h-16' source={require('../../assets/icons/Facial.png')} />
              <Text >Facial</Text>
            </View>
            <View className='flex flex-col justify-center items-center'>
              <Image className='w-16 h-16' source={require('../../assets/icons/Gardener.png')} />
              <Text >Gardener</Text>
            </View>
            <View className='flex flex-col justify-center items-center'>
              <Image className='w-16 h-16' source={require('../../assets/icons/painter.png')} />
              <Text >Painter</Text>
            </View>
            <View className='flex flex-col justify-center items-center'>
              <Image className='w-16 h-16' source={require('../../assets/icons/Yoga trainer.png')} />
              <Text >Yoga Trainer</Text>
            </View>
          </View>
        </ScrollView>
      </SafeAreaView>
  )
}