import pygame
import numpy as np
from sklearn import svm
import pandas as pd
import matplotlib.pyplot as plt
from pygame import QUIT

COLOR_PINK = 'pink'
COLOR_GREEN = 'green'
COLOR_RED = 'red'

def drawCircle(screen, x, y, color=COLOR_PINK):
    pygame.draw.circle(screen, color, (x, y), 5)

model = svm.SVC(kernel='linear')
screen = pygame.display.set_mode((500, 500))

is_running = True
is_start_svm = False
x_data = []
y_data = []
target = []
while is_running:
    for event in pygame.event.get():
        if event.type == pygame.MOUSEBUTTONDOWN:
            if not is_start_svm:
                (x, y) = pygame.mouse.get_pos()
                x_data.append(x)
                y_data.append(y)
                if event.button == 1:
                    drawCircle(screen, x, y, COLOR_RED)
                    target.append(0)
                elif event.button == 3:
                    drawCircle(screen, x, y, COLOR_GREEN)
                    target.append(1)
                pygame.display.flip()
            if is_start_svm:
                new_data = []
                (x, y) = pygame.mouse.get_pos()
                new_point = new_data.append([x, y])
                predictions_poly = model.predict(new_data)
                if predictions_poly[0] == 0:
                    drawCircle(screen, x, y, COLOR_RED)
                else:
                    drawCircle(screen, x, y, COLOR_GREEN)
            pygame.display.flip()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                is_start_svm = True
                df_x = pd.DataFrame(data=x_data)
                df_y = pd.DataFrame(data=y_data)
                df_target = pd.DataFrame(data=target)
                data_frame = pd.concat([df_x, df_y], ignore_index=True, axis=1)
                data_frame = pd.concat([data_frame, df_target], ignore_index=True, axis=1)

                data_frame.columns = ['x', 'y', 'target']

                features = data_frame[['x', 'y']]
                label = data_frame['target']
                features_values = features.values
                target_value = label.values
                length = len(features_values)

                print(features_values)

                model.fit(features_values, target_value)

                fig, ax = plt.subplots(figsize=(12, 7))
                xx = np.linspace(-1, max(features['x']) + 1, length)
                yy = np.linspace(0, max(features['y']) + 1, length)
                YY, XX = np.meshgrid(yy, xx)
                xy = np.vstack([XX.ravel(), YY.ravel()]).T
                colors = np.where(target_value == 1, '#00FF00', '#FF0000')
                ax.scatter(features['x'], features['y'], c=colors)
                Z = model.decision_function(xy).reshape(XX.shape)
                print(Z)
                ax.contour(XX, YY, Z, colors='k', levels=[0], alpha=0.5, linestyles=['-'])
                plt.show()
        if event.type == QUIT:
            pygame.quit()