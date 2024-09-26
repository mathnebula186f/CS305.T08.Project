import { View, Text, ScrollView, TouchableOpacity, Image } from 'react-native'
import React, { useContext, useState } from 'react'
import { categories } from '../constants'
import { useNavigation } from "@react-navigation/native";
import { AuthContext } from '../context/AuthContext';

// Helper function to dynamically resolve image names
const resolveImage = (imageName) => {
    switch (imageName) {
        case 'image1': return require('../assets/other_icon/carpenter.png');
        case 'image2': return require('../assets/other_icon/Barber.png');
        case 'image3': return require('../assets/other_icon/Car Service.png');
        case 'image4': return require('../assets/other_icon/chef.png');
        case 'image5': return require('../assets/other_icon/Chimney Sweep.png');
        case 'image6': return require('../assets/other_icon/manicure.png');
        case 'image7': return require('../assets/other_icon/Pest Control.png');
        case 'image8': return require('../assets/other_icon/plumber.png');
        // case 'image9': return require('../assets/icon5.jpg');
        // case 'image10': return require('../assets/icon6.jpg');
        // Add more cases for other image names
        default: return require('../assets/tp1.jpg');
    }
};

export default function Categories() {
    const [activeCategory, setActiveCategory] = useState(null);
    const navigation = useNavigation();
    const {logout} =useContext(AuthContext)

    return (
        <View className='mt-2'>
            <ScrollView
                horizontal
                showsHorizontalScrollIndicator={false}
                className = 'px-4'
            >
                {categories.map((category, index) => {
                    let isActive = category.id === activeCategory;
                    let btnStyle = isActive ? { backgroundColor: 'blue' } : { backgroundColor: 'lightgray' };
                    let textStyle = isActive ? { fontWeight: 'bold', color: 'darkgray' } : { color: 'gray' };

                    // Resolve image source using the helper function
                    const categoryImage = resolveImage(category.image);

                    return (
                        <TouchableOpacity
                            key={index}
                            onPress={() => { navigation.navigate('WorkerInfo',{service:category.name}) }}
                            className='align-center mx-2'
                        >
                            <View className='rounded-full border border-gray-300 w-20 h-20 bg-gray-100'>
                                <Image className='w-12 h-12 m-auto' source={categoryImage} />
                            </View>
                            <Text style={{ ...textStyle, marginTop: 3 }} className='text-center text-xs'>{category.name}</Text>
                        </TouchableOpacity>
                    );
                })}
            </ScrollView>
        </View>
    );
}
