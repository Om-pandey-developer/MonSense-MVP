/**
 * MonSense Global Application Context
 * Manages location navigation (State -> District -> Block),
 * Demo Mode vs Live API Mode toggle, and cross-component synchronization.
 */

import { createContext, useContext, useState, useEffect, useMemo, useCallback } from 'react';
import { mockData, DISTRICT_BOUNDS_MAP, STATE_BOUNDS_MAP } from '../services/mockData';

const AppContext = createContext(null);

export const SUPPORTED_STATES = [
  { code: 'MH', name: 'Maharashtra', name_local: 'महाराष्ट्र' },
  { code: 'KA', name: 'Karnataka', name_local: 'ಕರ್ನಾಟಕ' },
  { code: 'GJ', name: 'Gujarat', name_local: 'ગુજરાત' },
  { code: 'MP', name: 'Madhya Pradesh', name_local: 'मध्य प्रदेश' },
  { code: 'PB', name: 'Punjab', name_local: 'ਪੰਜਾਬ' },
  { code: 'UP', name: 'Uttar Pradesh', name_local: 'उत्तर प्रदेश' },
  { code: 'AP', name: 'Andhra Pradesh', name_local: 'ఆంధ్రప్రదేశ్' },
  { code: 'AR', name: 'Arunachal Pradesh', name_local: 'অৰুণাচল প্ৰদেশ' },
  { code: 'AS', name: 'Assam', name_local: 'অসম' },
  { code: 'BR', name: 'Bihar', name_local: 'बिहार' },
  { code: 'CG', name: 'Chhattisgarh', name_local: 'छत्तीसगढ़' },
  { code: 'GA', name: 'Goa', name_local: 'गोंय' },
  { code: 'HR', name: 'Haryana', name_local: 'हरियाणा' },
  { code: 'HP', name: 'Himachal Pradesh', name_local: 'हिमाचल प्रदेश' },
  { code: 'JH', name: 'Jharkhand', name_local: 'झारखंड' },
  { code: 'KL', name: 'Kerala', name_local: 'കേരളം' },
  { code: 'MN', name: 'Manipur', name_local: 'মণিপুর' },
  { code: 'ML', name: 'Meghalaya', name_local: 'मेघालय' },
  { code: 'MZ', name: 'Mizoram', name_local: 'मिज़ोरम' },
  { code: 'NL', name: 'Nagaland', name_local: 'नागालैंड' },
  { code: 'OD', name: 'Odisha', name_local: 'ଓଡ଼ିଶା' },
  { code: 'RJ', name: 'Rajasthan', name_local: 'राजस्थान' },
  { code: 'SK', name: 'Sikkim', name_local: 'सिक्किम' },
  { code: 'TN', name: 'Tamil Nadu', name_local: 'தமிழ்நாடு' },
  { code: 'TS', name: 'Telangana', name_local: 'తెలంగాణ' },
  { code: 'TR', name: 'Tripura', name_local: 'ত্রিপুরা' },
  { code: 'UK', name: 'Uttarakhand', name_local: 'उत्तराखण्ड' },
  { code: 'WB', name: 'West Bengal', name_local: 'पश्चिमবঙ্গ' },
  { code: 'DL', name: 'Delhi (NCT)', name_local: 'दिल्ली' },
  { code: 'JK', name: 'Jammu & Kashmir', name_local: 'جموں و کشمیر' },
];

export const DISTRICT_BOUNDS = DISTRICT_BOUNDS_MAP;

export function AppProvider({ children }) {
  // Navigation & Location Selection
  const [selectedStateCode, setSelectedStateCode] = useState('MH');
  const [selectedDistrict, setSelectedDistrictState] = useState('MH-PUN');
  const [selectedBlock, setSelectedBlockState] = useState('MH-PUN-BAR');

  // Mode Selection: false = Demo Presets (stable offline hackathon mode), true = Live API
  const [isLiveMode, setIsLiveMode] = useState(false);

  // Hierarchy Data
  const [hierarchy, setHierarchy] = useState(null);
  const [states, setStates] = useState(SUPPORTED_STATES);
  const [districts, setDistricts] = useState([]);
  const [blocks, setBlocks] = useState([]);

  // Load Hierarchy when state or live mode changes
  useEffect(() => {
    async function loadHierarchy() {
      if (isLiveMode) {
        try {
          const res = await fetch(`/api/v1/locations/hierarchy-with-bounds?state_code=${selectedStateCode}`);
          if (res.ok) {
            const data = await res.json();
            setHierarchy(data);
            if (data.states && data.states.length > 0) setStates(data.states);
            if (data.districts) setDistricts(data.districts);
            if (data.blocks) setBlocks(data.blocks);
            return;
          }
        } catch (e) {
          console.warn('Backend hierarchy fetch failed, falling back to mock presets', e);
        }
      }
      // Demo preset fallback
      const hData = mockData.getHierarchyWithBounds(selectedStateCode);
      setHierarchy(hData);
      if (hData.states) setStates(hData.states);
      setDistricts(hData.districts || []);
      setBlocks(hData.blocks || []);
    }
    loadHierarchy();
  }, [isLiveMode, selectedStateCode]);

  // Selected State object
  const currentStateObj = useMemo(() => {
    return states.find((s) => s.code === selectedStateCode || s.name === selectedStateCode) || SUPPORTED_STATES[0];
  }, [states, selectedStateCode]);

  const selectedState = currentStateObj.name;

  // Handle State Selection with automatic cascading to first district & block
  const setSelectedState = useCallback((stateIdentifier) => {
    const matchedState = states.find(
      (s) => s.code === stateIdentifier || s.name === stateIdentifier
    ) || SUPPORTED_STATES[0];

    setSelectedStateCode(matchedState.code);

    // Get cascading districts & blocks for the new state
    const hData = mockData.getHierarchyWithBounds(matchedState.code);
    const newDistricts = hData.districts || [];
    const newBlocks = hData.blocks || [];

    setDistricts(newDistricts);
    setBlocks(newBlocks);

    if (newDistricts.length > 0) {
      const firstDist = newDistricts[0];
      setSelectedDistrictState(firstDist.code);
      const childBlocks = newBlocks.filter((b) => b.parent_id === firstDist.id || b.code.startsWith(firstDist.code));
      if (childBlocks.length > 0) {
        setSelectedBlockState(childBlocks[0].code);
      }
    }
  }, [states]);

  // Current district blocks
  const currentDistrictBlocks = useMemo(() => {
    if (!blocks || blocks.length === 0) return [];
    const dist = districts.find((d) => d.code === selectedDistrict);
    if (!dist) return blocks;
    return blocks.filter((b) => b.parent_id === dist.id || b.code.startsWith(selectedDistrict));
  }, [blocks, districts, selectedDistrict]);

  // Current district object
  const currentDistrictObj = useMemo(() => {
    return districts.find((d) => d.code === selectedDistrict) || districts[0] || {
      name: 'Pune',
      code: 'MH-PUN',
    };
  }, [districts, selectedDistrict]);

  // Current block object
  const currentBlockObj = useMemo(() => {
    return blocks.find((b) => b.code === selectedBlock) || blocks[0] || {
      name: 'Baramati',
      code: 'MH-PUN-BAR',
    };
  }, [blocks, selectedBlock]);

  // Current bounding box (district or state)
  const districtBounds = useMemo(() => {
    if (DISTRICT_BOUNDS_MAP[selectedDistrict]) {
      return DISTRICT_BOUNDS_MAP[selectedDistrict];
    }
    if (STATE_BOUNDS_MAP[selectedStateCode]) {
      return STATE_BOUNDS_MAP[selectedStateCode];
    }
    return [[18.0, 73.3], [19.3, 75.1]];
  }, [selectedDistrict, selectedStateCode]);

  const stateBounds = useMemo(() => {
    return STATE_BOUNDS_MAP[selectedStateCode] || [[15.6, 72.6], [22.0, 80.9]];
  }, [selectedStateCode]);

  // Change District & Auto-select first child block
  const setSelectedDistrict = useCallback((distCode) => {
    setSelectedDistrictState(distCode);
    const dist = districts.find((d) => d.code === distCode);
    if (dist && blocks) {
      const childBlocks = blocks.filter((b) => b.parent_id === dist.id || b.code.startsWith(distCode));
      if (childBlocks.length > 0) {
        setSelectedBlockState(childBlocks[0].code);
      }
    }
  }, [districts, blocks]);

  const setSelectedBlock = useCallback((blockCode) => {
    setSelectedBlockState(blockCode);
    // Sync district if block belongs to different district
    const matchingBlock = blocks.find((b) => b.code === blockCode);
    if (matchingBlock && matchingBlock.parent_id) {
      const parentDist = districts.find((d) => d.id === matchingBlock.parent_id);
      if (parentDist && parentDist.code !== selectedDistrict) {
        setSelectedDistrictState(parentDist.code);
      }
    }
  }, [blocks, districts, selectedDistrict]);

  const toggleLiveMode = useCallback(() => {
    setIsLiveMode((prev) => !prev);
  }, []);

  const value = {
    selectedState,
    selectedStateCode,
    setSelectedState,
    states,
    selectedDistrict,
    setSelectedDistrict,
    selectedBlock,
    setSelectedBlock,
    isLiveMode,
    setIsLiveMode,
    toggleLiveMode,
    hierarchy,
    districts,
    blocks,
    currentDistrictBlocks,
    currentDistrictObj,
    currentBlockObj,
    districtBounds,
    stateBounds,
  };

  return <AppContext.Provider value={value}>{children}</AppContext.Provider>;
}

export function useApp() {

  const context = useContext(AppContext);
  if (!context) {
    throw new Error('useApp must be used within an AppProvider');
  }
  return context;
}
