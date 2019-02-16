# -*- mode: python -*-

block_cipher = None


a = Analysis(['stamp_cmd.py'],
             pathex=['/home/qiime/Dropbox/Work/Btools/stamp_cmd'],
             binaries=[],
             datas=[('stamp', 'stamp')],
             hiddenimports=['stamp.plugins.groups.plots.BarPlot', 'stamp.plugins.groups.plots.BoxPlot', 'stamp.plugins.groups.plots.ExtendedErrorBar', 'stamp.plugins.groups.plots.HeatmapPlot', 'stamp.plugins.groups.plots.pcaPlot', 'stamp.plugins.groups.plots.ScatterPlot', 'stamp.plugins.groups.effectSizeFilters.DiffBetweenProp', 'stamp.plugins.groups.effectSizeFilters.RatioProportions', 'stamp.plugins.groups.statisticalTests.Ttest', 'stamp.plugins.groups.statisticalTests.Welch', 'stamp.plugins.groups.statisticalTests.White', 'stamp.plugins.common.multipleComparisonCorrections.BenjaminiHochbergFDR', 'stamp.plugins.common.multipleComparisonCorrections.Bonferroni', 'stamp.plugins.common.multipleComparisonCorrections.NoCorrection', 'stamp.plugins.common.multipleComparisonCorrections.Sidak', 'stamp.plugins.common.multipleComparisonCorrections.StoreyFDR'],
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher)
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          a.binaries,
          a.zipfiles,
          a.datas,
          name='stamp_cmd',
          debug=False,
          strip=False,
          upx=True,
          console=True )
