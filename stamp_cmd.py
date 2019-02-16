#! /usr/bin/env python2
__version__ = "1.5.0"
import os
import sys
import argparse
from itertools import combinations
from importlib import import_module
from distutils.sysconfig import get_python_lib

import matplotlib as mpl
mpl.use('agg')

from PyQt4 import QtGui, QtCore

from stamp.metagenomics.fileIO.StampIO import StampIO
from stamp.metagenomics.fileIO.MetadataIO import MetadataIO
from stamp.metagenomics.stats.GroupStatsTests import GroupStatsTests
from stamp.metagenomics.TableHelper import SortTableStrCol

from stamp.plugins.PlotsManager import PlotsManager
from stamp.plugins.groups.AbstractGroupPlotPlugin import AbstractGroupPlotPlugin


def load_data(profileFile, metadataFile):
    # read profiles from file
    profileTree = None
    try:
        stampIO = StampIO({})
        profileTree, errMsg = stampIO.read(profileFile)
        if errMsg != None:
            print 'Error reading profile file', errMsg
            return
    except:
        print 'Error reading profile file:', profileFile
        return
    metadata = None
    if metadataFile != '':
        try:
            metadataIO = MetadataIO({})
            metadata, warningMsg = metadataIO.read(metadataFile, profileTree)
            # metadata.setActiveField(metadataField, profileTree)
            if warningMsg != None:
                print 'Metadata warnings', warningMsg
        except:
            print 'Error reading metadata file:', metadataFile
            return
    return profileTree, metadata

# groupStatTestDict = loadPlugins(preferences, 'plugins/groups/statisticalTests/')
def loadPlugins(preferences, pluginFolder):
    pluginModulePath = 'stamp.' + pluginFolder.replace('/', '.')
    #pluginFolder = os.path.join(get_python_lib(), 'stamp', pluginFolder)
    pluginFolder = import_module(pluginModulePath[:-1]).__path__[0]
    d = {}
    for filename in os.listdir(pluginFolder):
        if os.path.isdir(os.path.join (pluginFolder, filename)):
            continue
        extension = filename[filename.rfind('.')+1:len(filename)]
        if extension == 'py' and filename != '__init__.py':
            pluginModule = filename[0:filename.rfind('.')]
            theModule = import_module(pluginModulePath + pluginModule)
            theClass = getattr(theModule, pluginModule)
            theObject = theClass(preferences)
            d[theObject.name] = theObject
    return d

# plotDict = loadPlots(preferences, 'plugins/groups/plots/')
def loadPlots(preferences, pluginFolder):
    pluginModulePath = 'stamp.' + pluginFolder.replace('/', '.')
    #pluginFolder = os.path.join(get_python_lib(), 'stamp', pluginFolder)
    pluginFolder = import_module(pluginModulePath[:-1]).__path__[0]
    plotDict = {}
    for filename in os.listdir(pluginFolder):
        if os.path.isdir(os.path.join (pluginFolder, filename)):
            continue
        extension = filename[filename.rfind('.')+1:len(filename)]	
        if extension == 'py' and filename != '__init__.py':
            pluginModule = filename[0:filename.rfind('.')]
            theModule = import_module(pluginModulePath + pluginModule)
            theClass = getattr(theModule, pluginModule)
            plot = theClass(preferences)
            plotDict[plot.name] = plot
    return plotDict


def initLegend(profileTree, metadata, field):
    groupColours = [QtGui.QColor(128, 177, 211), QtGui.QColor(253, 180, 98),
                    QtGui.QColor(179, 222, 105), QtGui.QColor(190, 186, 218), 
                    QtGui.QColor(141, 211, 199), QtGui.QColor(251, 128, 114),
                    QtGui.QColor(252, 205, 229), QtGui.QColor(127,127,127),
                    QtGui.QColor(188, 128, 189), QtGui.QColor(204, 235, 197)]
    groupColourDict = {}
    # this populates profileTree.groupDict
    metadata.setActiveField(field, profileTree)
    # add legend items
    index = 0
    for name in sorted(profileTree.groupDict.keys()):
        samples = set(sorted(profileTree.groupDict[name]))
        samples = list(samples.intersection(set(metadata.activeSamples)))
        # force groups with no active samples to be inactive
        if len(samples) == 0:
            profileTree.groupActive[name] = False
        else:
            profileTree.groupActive[name] = True
        if index == len(groupColours):
            groupColours.append(QtGui.QColor(0, 0, 0))
        colour = groupColours[index]
        groupColourDict[name] = colour
        index += 1
    return groupColourDict

if __name__ == '__main__':
    parser = argparse.ArgumentParser(formatter_class=lambda prog: argparse.ArgumentDefaultsHelpFormatter(prog, max_help_position=36, width=120))
    parser.add_argument('-i', '--profile', required=True, help='Path to the profile file')
    parser.add_argument('-g', '--metadata', required=True, help='Path to the group metadata file')
    parser.add_argument('-d', '--output', default='output', help='Output directory')
    parser.add_argument('-p', '--plot', default='{g1}-vs-{g2}.psig.png', help='Plot filename template, supported filetypes: png, pdf, ps, eps, svg')
    parser.add_argument('-t', '--table', default='{g1}-vs-{g2}.test.xls', help='Table filename template')
    parser.add_argument('-r', '--dpi', type=int, default=500, help='Plot DPI (dots per inch)')
    parser.add_argument('-v', '--version', action='version', version='%(prog)s ' + __version__)
    args = parser.parse_args()
    # user input
    profileFile = 'otu.g.spf'
    metadataFile = 'Grouping.txt'
    saveFolder = 'output'
    savePlotTemplate = '{g1}-vs-{g2}.psig.png'
    saveTableTemplate = '{g1}-vs-{g2}.test.xls'
    dpi = 500

    profileFile = args.profile
    metadataFile = args.metadata
    saveFolder = args.output
    savePlotTemplate = args.plot
    saveTableTemplate = args.table
    dpi = args.dpi

    # setup default plot settings
    mpl.rcParams['font.size'] = 8
    mpl.rcParams['axes.titlesize'] = 8
    mpl.rcParams['axes.labelsize'] = 8
    mpl.rcParams['xtick.labelsize'] = 8
    mpl.rcParams['ytick.labelsize'] = 8
    mpl.rcParams['legend.fontsize'] = 8

    # initialize preferences
    preferences = {}
    settings = QtCore.QSettings("BeikoLab", "STAMP")
    preferences['Settings'] = settings
    preferences['Executable directory'] = sys.path[0]
    preferences['Pseudocount'] = settings.value('Preferences/Pseudocount', 0.5).toDouble()[0]
    preferences['Replicates'] = settings.value('Preferences/Replicates', 1000).toInt()[0]
    preferences['Truncate feature names'] = settings.value('Preferences/Truncate feature names', True).toBool()
    preferences['Length of truncated feature names'] = settings.value('Preferences/Length of truncated feature names', 50).toInt()[0]
    preferences['Axes colour'] = QtGui.QColor(settings.value('Preferences/Axes colour', '#7f7f7f'))
    preferences['All other samples colour'] = QtGui.QColor(settings.value('Preferences/All other samples colour', '#7f7f7f'))
    preferences['Minimum reported p-value exponent'] = settings.value('Preferences/Minimum reported p-value exponent', -15).toDouble()[0]
    preferences['Sample 1 colour'] = QtGui.QColor(128, 177, 211)
    preferences['Sample 2 colour'] = QtGui.QColor(253, 180, 98)
    preferences['Group colours'] = {}
    preferences['Highlighted sample features'] = []
    preferences['Highlighted group features'] = []
    preferences['Highlighted multiple group features'] = []
    preferences['Selected group feature'] = ''
    preferences['Selected multiple group feature'] = ''

    defaultPlot = 'PCA plot'
    plotDict = loadPlots(preferences, 'plugins/groups/plots/')
    groupPlotOptions = sorted(plotDict.keys())
    # ['Bar plot', 'Box plot', 'Extended error bar', 'Heatmap plot', 'PCA plot', 'Scatter plot']
    groupPlotIndex = 2
    groupPlot = groupPlotOptions[groupPlotIndex]
    
    profileTree, metadata = load_data(profileFile, metadataFile)

    parentLevelOptions = ['Entire sample'] + profileTree.hierarchyHeadings
    parentLevel = parentLevelOptions[0]

    profileLevelOptions = profileTree.hierarchyHeadings
    profileLevelIndex = 0
    profileLevel = profileLevelOptions[profileLevelIndex]
    
    unclassifiedTreatmentOptions = ['Retain unclassified reads', 
    'Remove unclassified reads', 
    'Use only for calculating frequency profiles']
    unclassifiedTreatment = unclassifiedTreatmentOptions[0]

    typeOfTestOptions = ['Multiple groups', 'Two groups', 'Two samples']
    typeOfTest = typeOfTestOptions[1]

    groupFieldOptions = metadata.getFeatures()
    groupField = groupFieldOptions[0]

    # setup group legend
    groupColorDict = initLegend(profileTree, metadata, groupField)
    preferences['Group colours'] = groupColorDict

    samples = sorted(profileTree.sampleNames)
    groups = sorted(profileTree.groupActive.keys())
    # populateGroupComboBoxes
    #groupName1 = groups[2]
    #groupName2 = groups[4]
    for groupName1, groupName2 in combinations(groups, 2):
    #for groupName1, groupName2 in [(groups[0], groups[2])]:

        # indicate the hierarchical level of interest has changed
        ## groupHierarchicalLevelsChanged()
        groupHighlightHierarchyOptions = ['None'] + profileTree.hierarchyHeadings[0:profileLevelIndex + 1]
        groupHighlightHierarchyIndex = 0
        groupHighlightHierarchy = groupHighlightHierarchyOptions[groupHighlightHierarchyIndex]

        groupHighlightFeatureOptions = []


        groupEffectSizeDict = loadPlugins(preferences, 'plugins/groups/effectSizeFilters/')
        # 'Ratio of proportions', 'Difference between proportions'
        groupEffectSizeMeasure1Options = sorted(groupEffectSizeDict.keys())
        groupEffectSizeMeasure1Index = 1
        groupEffectSizeMeasure1 = groupEffectSizeMeasure1Options[groupEffectSizeMeasure1Index]

        groupEffectSizeMeasure2Options = sorted(groupEffectSizeDict.keys())
        groupEffectSizeMeasure2Index = 0
        groupEffectSizeMeasure2 = groupEffectSizeMeasure2Options[groupEffectSizeMeasure2Index]

        groupStatTestDict = loadPlugins(preferences, 'plugins/groups/statisticalTests/')
        # "White's non-parametric t-test", "Welch's t-test", 't-test (equal variance)'
        groupStatTest = "Welch's t-test"

        multCompDict = loadPlugins(preferences, 'plugins/common/multipleComparisonCorrections/')
        # 'Benjamini-Hochberg FDR', 'Sidak', 'Storey FDR', 'Bonferroni', 'No correction'
        groupMultCompMethodOptions = sorted(multCompDict.keys())
        # ['Benjamini-Hochberg FDR', 'Bonferroni', 'No correction', 'Sidak', 'Storey FDR']
        groupMultCompMethodIndex = 2 # 'No correction'
        groupMultCompMethod = groupMultCompMethodOptions[groupMultCompMethodIndex]

        groupSignTestTypeOptions = ['One-sided', 'Two-sided']
        groupSignTestTypeIndex = 1
        groupSignTestType = groupSignTestTypeOptions[groupSignTestTypeIndex]

        groupStatsTest = GroupStatsTests(preferences)

        # run statistics
        ### groupRunTest()
        # groupTestConfIntervMethods()
        # populate combo box with CI methods compatible with current hypothesis test
        test = groupStatTestDict[groupStatTest]
        groupConfIntervMethodOptions = test.confIntervMethods
        # ["DP: Welch's inverted"]
        groupConfIntervMethod = groupConfIntervMethodOptions[0]

        groupNominalCoverageOptions = ['0.90', '0.95', '0.98', '0.99', '0.999']
        groupNominalCoverage = groupNominalCoverageOptions[1]

        # show progress of test
        print 'Running two-group statistical test ({0}, {1}),'.format(groupName1, groupName2),

        # create profile
        groupProfile = profileTree.createGroupProfile(groupName1, groupName2, parentLevel, profileLevel, metadata, unclassifiedTreatment)

        # run significance test
        groupStatsTest.run(test, groupSignTestType, groupConfIntervMethod, float(groupNominalCoverage), groupProfile)

        # apply multiple test correction
        groupStatsTest.results.performMultCompCorrection(multCompDict[groupMultCompMethod])

        # apply filters
        #### groupApplyFilters()
        selectedFeatures = []
        if not selectedFeatures:
            groupStatsTest.results.selectAllFeautres()
            selectedFeatures = groupStatsTest.results.getSelectedFeatures()

        inactiveFeatures = ['Others']
        selectedFeatures = list(set(selectedFeatures) - set(inactiveFeatures))
        groupStatsTest.results.setSelectedFeatures(selectedFeatures)


        # perform filtering
        groupEnableSignLevelFilter = True
        groupSignLevelFilter = 0.05
        if not groupSignLevelFilter:
            groupSignLevelFilter = None

        # sequence filtering
        groupEnableSeqFilter = False
        groupSeqFilterOptions = ['maximum', 'minimum', 'independent, maximum', 'independent, minimum']
        groupSeqFilterIndex = 0
        groupSeqFilter = groupSeqFilterOptions[groupSeqFilterIndex]
        group1Filter = 5
        group2Filter = 5
        if not groupEnableSeqFilter:
            groupSeqFilter = None
            group1Filter = None
            group2Filter = None

        groupEnableParentSeqFilter = False
        groupParentSeqFilterOptions = ['maximum', 'minimum', 'independent, maximum', 'independent, minimum']
        groupParentSeqFilterIndex = 0
        groupParentSeqFilter = groupParentSeqFilterOptions[groupParentSeqFilterIndex]
        groupParentGroup1Filter = 1
        groupParentGroup2Filter = 1
        if not groupEnableParentSeqFilter:
            groupParentSeqFilter = None
            groupParentGroup1Filter = None
            groupParentGroup2Filter = None

        # effect size filters
        groupEnableEffectSizeFilter1 = False
        if groupEnableEffectSizeFilter1:
            groupMinEffectSize1 = 1.0
        else:
            groupEffectSizeMeasure1 = None
            groupMinEffectSize1 = None

        groupEnableEffectSizeFilter2 = False
        if groupEnableEffectSizeFilter2:
            groupMinEffectSize2 = 2.0
        else:
            groupEffectSizeMeasure2 = None
            groupMinEffectSize2 = None

        effectSizeOperatorOptions = ['OR', 'AND']
        effectSizeOperatorIndex = 0
        effectSizeOperator = effectSizeOperatorOptions[effectSizeOperatorIndex]

        groupStatsTest.results.filterFeatures(groupSignLevelFilter, groupSeqFilter, group1Filter, group2Filter, groupParentSeqFilter, groupParentGroup1Filter, groupParentGroup2Filter, groupEffectSizeMeasure1, groupMinEffectSize1, effectSizeOperator, groupMinEffectSize2, groupMinEffectSize2)

        # update table summarizing statistical results
        #self.groupFeaturesTableUpdate()
        #self.groupTable.updateTable(self.groupStatsTest)

        # update plots
        ##### groupPlotUpdate()
        # update plot
        if groupStatsTest.results.activeData != []:
            print 'Plotting:',
            plotDict[groupPlot].sortingField = 'Effect sizes'
            plotDict[groupPlot].figHeightPerRow = 0.55
            plotDict[groupPlot].legendPos = 2
            plotDict[groupPlot].bShowCorrectedPvalues = False
            plotDict[groupPlot].plot(groupProfile, groupStatsTest.results)
            # saveFolder = 'output'
            # savePlotTemplate = '{g1}-vs-{g2}.png'
            # saveTableTemplate = '{g1}-vs-{g2}.test.xls'
            filename = os.path.join(saveFolder, savePlotTemplate.format(g1=groupName1, g2=groupName2))
            print '"{0}",'.format(filename),
            if not os.path.exists(os.path.dirname(filename)):
                try:
                    os.makedirs(os.path.dirname(filename))
                except OSError as exc: # Guard against race condition
                    if exc.errno != errno.EEXIST:
                        raise
            ext = filename[filename.rfind('.')+1:len(filename)]
            # dpi = 500
            if ext in ['png', 'pdf', 'ps', 'eps','svg']:
                plotDict[groupPlot].fig.savefig(filename, format=ext, dpi=dpi, facecolor='white', edgecolor='white')
            else:
                print 'Unsupported plot output format:', ext

            # Prepare table
            # ['Benjamini-Hochberg FDR', 'Bonferroni', 'No correction', 'Sidak', 'Storey FDR']
            print 'Sidak table:',
            groupMultCompMethodIndex = 3 # 'No correction'
            groupMultCompMethod = groupMultCompMethodOptions[groupMultCompMethodIndex]
            # run significance test
            groupStatsTest.run(test, groupSignTestType, groupConfIntervMethod, float(groupNominalCoverage), groupProfile)

            # apply multiple test correction
            groupStatsTest.results.performMultCompCorrection(multCompDict[groupMultCompMethod])
            groupStatsTest.results.setSelectedFeatures(selectedFeatures)
            groupStatsTest.results.filterFeatures(groupSignLevelFilter, groupSeqFilter, group1Filter, group2Filter, groupParentSeqFilter, groupParentGroup1Filter, groupParentGroup2Filter, groupEffectSizeMeasure1, groupMinEffectSize1, effectSizeOperator, groupMinEffectSize2, groupMinEffectSize2)
            
            tableData, tableHeadings = groupStatsTest.results.tableData(False)
            tableData = SortTableStrCol(tableData, 0)
            
            filename = os.path.join(saveFolder, saveTableTemplate.format(g1=groupName1, g2=groupName2))
            print '"{0}"'.format(filename),
            fout = open(filename, 'w')
            for heading in tableHeadings:
                fout.write(heading + '\t')
            fout.write('\n')
            for row in tableData:
                for entry in row:
                    fout.write(str(entry) + '\t')
                fout.write('\n')
            fout.close()
            print 'DONE.'
        else:
            print 'No Active Data, SKIP.'
        
